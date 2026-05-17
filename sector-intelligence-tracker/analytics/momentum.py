import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MomentumReport(BaseModel):
    sector: str
    composite_score: float = Field(..., description="Weighted composite score (0-100)")
    regime: str = Field(..., description="Market/sector regime (bull/bear/neutral)")
    signal_deltas: Dict[str, Dict[str, float]] = Field(..., description="WoW and MoM deltas for each metric")
    divergence_flags: List[str] = Field(..., description="Detected anomaly or divergence flags")
    metrics: Dict[str, float] = Field(..., description="Current raw normalized scores (0-10)")

class MomentumScorer:
    @staticmethod
    def normalize_metrics(raw_json: str) -> Dict[str, float]:
        """Normalizes raw data from a snapshot into 0-10 scores."""
        try:
            data = json.loads(raw_json)
        except Exception:
            # Fallback if raw_json is empty or invalid
            return {
                "trend_score": 5.0,
                "news_sentiment": 5.0,
                "hiring_velocity": 5.0,
                "app_health": 5.0,
                "employer_health": 5.0
            }

        # 1. Trend Score (Google Trends)
        trend_score = 5.0
        trends_data = data.get("trends", {}).get("data", [])
        if isinstance(trends_data, list) and len(trends_data) > 0:
            # List of records: [{"date": "...", "Co1": val, "Co2": val}]
            # We take the latest record and average the interest values
            latest = trends_data[-1]
            vals = [val for key, val in latest.items() if key != "date" and isinstance(val, (int, float))]
            if vals:
                trend_score = min(10.0, max(0.0, sum(vals) / len(vals) / 10.0))
        elif isinstance(trends_data, dict) and trends_data:
            # Alternative dict format
            vals = []
            for co, dates_dict in trends_data.items():
                if isinstance(dates_dict, dict) and dates_dict:
                    latest_val = list(dates_dict.values())[-1]
                    if isinstance(latest_val, (int, float)):
                        vals.append(latest_val)
            if vals:
                trend_score = min(10.0, max(0.0, sum(vals) / len(vals) / 10.0))

        # 2. News Sentiment
        news_sentiment = 5.0
        sentiment_data = data.get("sentiment", {}).get("data", {})
        if sentiment_data:
            # sentiment_data is {co: {"positive_pct": ...}}
            positives = []
            for co, info in sentiment_data.items():
                if isinstance(info, dict) and "positive_pct" in info:
                    positives.append(info["positive_pct"])
            if positives:
                news_sentiment = min(10.0, max(0.0, sum(positives) / len(positives) / 10.0))

        # 3. Hiring Velocity (LinkedIn Jobs)
        hiring_velocity = 5.0
        jobs_data = data.get("jobs", {}).get("data", {})
        if jobs_data:
            # jobs_data is {co: count}
            job_counts = [count for count in jobs_data.values() if isinstance(count, (int, float))]
            if job_counts:
                avg_jobs = sum(job_counts) / len(job_counts)
                hiring_velocity = min(10.0, max(0.0, avg_jobs / 30.0)) # normalise e.g. 300 jobs = 10.0

        # 4. App Store Health (ratings)
        app_health = 5.0
        ratings_data = data.get("ratings", {}).get("data", {})
        if ratings_data:
            # ratings_data is {co: {"rating": ...}}
            ratings = []
            for co, info in ratings_data.items():
                if isinstance(info, dict) and "rating" in info:
                    ratings.append(info["rating"])
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                app_health = min(10.0, max(0.0, avg_rating * 2.0)) # scale 0-5 to 0-10

        # 5. Employer Health (ambitionbox)
        employer_health = 5.0
        employer_data = data.get("employer", {}).get("data", {})
        if employer_data:
            # employer_data is {co: rating_float}
            ratings = [val for val in employer_data.values() if isinstance(val, (int, float))]
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                employer_health = min(10.0, max(0.0, avg_rating * 2.0)) # scale 0-5 to 0-10

        return {
            "trend_score": round(trend_score, 2),
            "news_sentiment": round(news_sentiment, 2),
            "hiring_velocity": round(hiring_velocity, 2),
            "app_health": round(app_health, 2),
            "employer_health": round(employer_health, 2)
        }

    @classmethod
    def score_sector(cls, sector_name: str, snapshots: List[Any]) -> MomentumReport:
        """Computes the quantitative momentum report for a sector based on snapshots."""
        if not snapshots:
            empty_metrics = {
                "trend_score": 5.0,
                "news_sentiment": 5.0,
                "hiring_velocity": 5.0,
                "app_health": 5.0,
                "employer_health": 5.0
            }
            return MomentumReport(
                sector=sector_name,
                composite_score=50.0,
                regime="neutral",
                signal_deltas={k: {"wow": 0.0, "mom": 0.0} for k in empty_metrics},
                divergence_flags=[],
                metrics=empty_metrics
            )

        # Sort snapshots by captured_at descending (latest first)
        sorted_snapshots = sorted(snapshots, key=lambda s: s.captured_at, reverse=True)
        latest_snapshot = sorted_snapshots[0]
        latest_metrics = cls.normalize_metrics(latest_snapshot.raw_json)

        # Find snapshots closest to 7 days and 30 days ago
        now = latest_snapshot.captured_at
        wow_snapshot = None
        mom_snapshot = None

        for s in sorted_snapshots[1:]:
            age = now - s.captured_at
            if wow_snapshot is None and age >= timedelta(days=5) and age <= timedelta(days=9):
                wow_snapshot = s
            if mom_snapshot is None and age >= timedelta(days=25) and age <= timedelta(days=35):
                mom_snapshot = s

        # If not found, use default lag metrics
        if wow_snapshot is None and len(sorted_snapshots) > 1:
            wow_snapshot = sorted_snapshots[min(len(sorted_snapshots) - 1, 3)] # fallback to an older snapshot
        if mom_snapshot is None and len(sorted_snapshots) > 1:
            mom_snapshot = sorted_snapshots[-1] # fallback to the oldest snapshot

        wow_metrics = cls.normalize_metrics(wow_snapshot.raw_json) if wow_snapshot else latest_metrics
        mom_metrics = cls.normalize_metrics(mom_snapshot.raw_json) if mom_snapshot else latest_metrics

        # Compute deltas
        signal_deltas = {}
        for key in latest_metrics:
            signal_deltas[key] = {
                "wow": round(latest_metrics[key] - wow_metrics[key], 2),
                "mom": round(latest_metrics[key] - mom_metrics[key], 2)
            }

        # Weighted composite score (0-10 scale, then multiplied by 10 to get 0-100 scale)
        composite_10 = (
            latest_metrics["trend_score"] * 0.30 +
            latest_metrics["news_sentiment"] * 0.25 +
            latest_metrics["hiring_velocity"] * 0.20 +
            latest_metrics["app_health"] * 0.15 +
            latest_metrics["employer_health"] * 0.10
        )
        composite_score = round(composite_10 * 10.0, 1)

        # WoW composite delta for regime detection
        wow_comp_10 = (
            wow_metrics["trend_score"] * 0.30 +
            wow_metrics["news_sentiment"] * 0.25 +
            wow_metrics["hiring_velocity"] * 0.20 +
            wow_metrics["app_health"] * 0.15 +
            wow_metrics["employer_health"] * 0.10
        )
        wow_composite = round(wow_comp_10 * 10.0, 1)
        wow_delta = composite_score - wow_composite

        # Determine Regime
        if composite_score >= 65.0 and wow_delta >= 0.0:
            regime = "bull"
        elif composite_score < 45.0 or wow_delta < -5.0:
            regime = "bear"
        else:
            regime = "neutral"

        # Anomaly / Divergence Detection
        divergence_flags = []
        
        # 1. Stealth Growth: high hiring but declining trends
        if latest_metrics["hiring_velocity"] >= 7.0 and signal_deltas["trend_score"]["wow"] < -0.5:
            divergence_flags.append("stealth_growth")
            
        # 2. Hype Bubble: high search trends but low hiring
        if latest_metrics["trend_score"] >= 8.0 and latest_metrics["hiring_velocity"] < 4.0:
            divergence_flags.append("hype_bubble")

        # 3. Product-Market Decoupling: declining app health while trends are stable or growing
        if signal_deltas["app_health"]["wow"] < -0.3 and signal_deltas["trend_score"]["wow"] >= 0.0:
            divergence_flags.append("product_decay")

        # 4. Toxic Scale: high app rating/health but extremely low employer health
        if latest_metrics["app_health"] >= 7.5 and latest_metrics["employer_health"] < 4.5:
            divergence_flags.append("toxic_scale")

        return MomentumReport(
            sector=sector_name,
            composite_score=composite_score,
            regime=regime,
            signal_deltas=signal_deltas,
            divergence_flags=divergence_flags,
            metrics=latest_metrics
        )

    @classmethod
    def backtest_sector(cls, sector_name: str, snapshots: List[Any]) -> List[Dict[str, Any]]:
        """Replays historical snapshots and scores them chronologically."""
        if not snapshots:
            return []
        # Sort chronologically
        sorted_snaps = sorted(snapshots, key=lambda s: s.captured_at)
        history = []
        for i in range(len(sorted_snaps)):
            sub_snaps = sorted_snaps[:i+1]
            report = cls.score_sector(sector_name, sub_snaps)
            history.append({
                "date": sorted_snaps[i].captured_at.strftime("%Y-%m-%d"),
                "score": report.composite_score
            })
        return history
