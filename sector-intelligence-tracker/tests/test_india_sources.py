"""
tests/test_india_sources.py
----------------------------
Unit tests for India-specific financial data harvesting.
"""

import pytest
import asyncio
from data.india_sources import fetch_india_financials, get_fallback_financials, FALLBACK_PROFILES

def test_fallback_financials():
    """Validates the static high-fidelity fallback database returns exact structures."""
    companies = ["Razorpay", "LatentView", "Groww"]
    data = get_fallback_financials(companies)
    
    assert "index_quote" in data
    assert "company_profiles" in data
    
    profiles = data["company_profiles"]
    assert len(profiles) == 3
    
    for c in companies:
        assert c in profiles
        p = profiles[c]
        assert "market_cap" in p
        assert "revenue_ttm" in p
        assert "paid_up_capital" in p
        assert "incorporation_date" in p
        assert isinstance(p["din_directors"], list)

@pytest.mark.asyncio
async def test_fetch_india_financials():
    """Validates the async aggregator with a quick 1-company query (limiting pacing sleep)."""
    companies = ["LatentView"]
    # Quick execution
    data = await fetch_india_financials(companies, "Analytics Consulting")
    
    assert "index_quote" in data
    assert "company_profiles" in data
    
    profiles = data["company_profiles"]
    assert "LatentView" in profiles
    
    p = profiles["LatentView"]
    assert p["market_cap"] > 0
    assert p["revenue_ttm"] > 0
    assert p["funding_stage"] == "Public (IPO)"
