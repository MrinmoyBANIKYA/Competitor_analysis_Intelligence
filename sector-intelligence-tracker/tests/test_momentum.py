import pytest
import json
from datetime import datetime, timedelta
from analytics.momentum import MomentumScorer, MomentumReport

class MockSnapshot:
    def __init__(self, captured_at: datetime, raw_json: str):
        self.captured_at = captured_at
        self.raw_json = raw_json

def make_raw_json(trend_vals, news_count, jobs_count, rating_val, ab_rating):
    # Matches structure returned by normalized_metrics in MomentumScorer
    # positive_pct is news_sentiment * 10
    pos_pct = 75
    return json.dumps({
        "trends": {"data": [{"date": "2026-05-01", "PhonePe": val} for val in trend_vals]},
        "sentiment": {"data": {"PhonePe": {"positive_pct": pos_pct}}},
        "jobs": {"data": {"PhonePe": jobs_count}},
        "ratings": {"data": {"PhonePe": {"rating": rating_val}}},
        "employer": {"data": {"PhonePe": ab_rating}}
    })

def test_bull_scenario():
    # Bull Scenario: strong performance and rising trends
    now = datetime.now()
    latest_snap = MockSnapshot(
        captured_at=now,
        raw_json=make_raw_json([85], 100, 250, 4.5, 4.2) # High scores
    )
    wow_snap = MockSnapshot(
        captured_at=now - timedelta(days=7),
        raw_json=make_raw_json([80], 90, 220, 4.4, 4.1) # slightly lower scores
    )
    
    report = MomentumScorer.score_sector("Fintech", [latest_snap, wow_snap])
    
    assert report.composite_score >= 65.0
    assert report.regime == "bull"
    assert not report.divergence_flags

def test_bear_scenario():
    # Bear Scenario: weak performance and declining trends
    now = datetime.now()
    latest_snap = MockSnapshot(
        captured_at=now,
        raw_json=make_raw_json([30], 20, 30, 3.2, 3.0) # low scores
    )
    wow_snap = MockSnapshot(
        captured_at=now - timedelta(days=7),
        raw_json=make_raw_json([45], 40, 50, 3.5, 3.2) # higher scores 1 week ago
    )
    
    report = MomentumScorer.score_sector("Fintech", [latest_snap, wow_snap])
    
    assert report.composite_score < 50.0
    assert report.regime == "bear"

def test_divergence_scenario():
    # Divergence Scenario (Stealth Growth): hiring velocity is extremely high, but search trends are declining
    now = datetime.now()
    latest_snap = MockSnapshot(
        captured_at=now,
        raw_json=make_raw_json([30], 80, 280, 4.0, 4.0) # Search trend = 3.0, hiring velocity = 9.3
    )
    wow_snap = MockSnapshot(
        captured_at=now - timedelta(days=7),
        raw_json=make_raw_json([45], 80, 280, 4.0, 4.0) # 1 week ago search trend was 4.5 (declined)
    )
    
    report = MomentumScorer.score_sector("Fintech", [latest_snap, wow_snap])
    
    assert "stealth_growth" in report.divergence_flags

def test_backtest_scenario():
    # Backtest Scenario: verify chronological history list
    now = datetime.now()
    snap1 = MockSnapshot(captured_at=now - timedelta(days=15), raw_json=make_raw_json([50], 50, 100, 4.0, 4.0))
    snap2 = MockSnapshot(captured_at=now - timedelta(days=7), raw_json=make_raw_json([60], 60, 150, 4.2, 4.1))
    snap3 = MockSnapshot(captured_at=now, raw_json=make_raw_json([75], 80, 200, 4.5, 4.3))
    
    history = MomentumScorer.backtest_sector("Fintech", [snap3, snap1, snap2]) # unordered input
    
    assert len(history) == 3
    assert history[0]["date"] == (now - timedelta(days=15)).strftime("%Y-%m-%d")
    assert history[2]["date"] == now.strftime("%Y-%m-%d")
    assert history[2]["score"] > history[0]["score"] # rising trend
