"""
data/fallback_data.py
---------------------
Realistic mock data for each sector used as fallback when scrapers fail.
"""

import pandas as pd
import datetime
import random

def get_fallback_trends(companies: list) -> pd.DataFrame:
    dates = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(365, 0, -7)]
    mock_data = {"date": dates}
    for co in companies:
        rng = random.Random(co)
        val = rng.randint(40, 60)
        walk = []
        for _ in dates:
            val = max(10, min(100, val + rng.randint(-8, 10)))
            walk.append(val)
        mock_data[co] = walk
    df = pd.DataFrame(mock_data).set_index("date")
    return df

def get_fallback_playstore(companies: list) -> dict:
    result = {}
    for co in companies:
        rng = random.Random(co)
        result[co] = {
            "rating": round(rng.uniform(3.8, 4.7), 1),
            "num_ratings": rng.randint(50000, 1000000)
        }
    return result

def get_fallback_linkedin(companies: list) -> dict:
    result = {}
    for co in companies:
        rng = random.Random(co)
        result[co] = rng.randint(50, 500)
    return result

def get_fallback_ambitionbox(companies: list) -> dict:
    result = {}
    for co in companies:
        rng = random.Random(co)
        result[co] = round(rng.uniform(3.5, 4.4), 1)
    return result

def get_fallback_news(companies: list) -> dict:
    result = {}
    for co in companies:
        rng = random.Random(co)
        result[co] = rng.randint(10, 150)
    return result

def get_fallback_sentiment(companies: list) -> dict:
    result = {}
    for co in companies:
        rng = random.Random(co)
        result[co] = {
            "positive_pct": rng.randint(60, 85),
            "negative_pct": rng.randint(5, 20),
            "neutral_pct": rng.randint(10, 20),
            "top_complaints": ["UI lag", "Login issues", "Slow response"],
            "review_count": rng.randint(100, 500)
        }
    return result
