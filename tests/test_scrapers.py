import pytest
import asyncio
import pandas as pd
import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock

# Add project root to sys.path
sys.path.append(os.path.join(os.getcwd(), "sector-intelligence-tracker"))

from data.scrapers import DataFetcher, SectorData, _get_cached_or_fetch

@pytest.mark.asyncio
async def test_fetch_all_success():
    """Test that fetch_all calls all 6 data sources and returns SectorData."""
    fetcher = DataFetcher()
    sector_config = {
        "name": "Fintech",
        "companies": ["Paytm"],
        "app_ids": {"Paytm": "com.paytm"},
        "linkedin_slugs": {"Paytm": "paytm"}
    }
    
    mock_res = {"data": pd.DataFrame({"val": [1]}), "status": "ok", "source_name": "Mock"}
    
    with patch("data.scrapers._get_cached_or_fetch", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_res
        
        results = await fetcher.fetch_all(sector_config, ["Paytm"], "fake_news_key")
        
        assert isinstance(results, SectorData)
        assert results.health_score == 100
        assert mock_fetch.call_count == 6  # trends, ratings, jobs, employer, news, sentiment

@pytest.mark.asyncio
async def test_fetch_all_partial_failure():
    """Test health score calculation when some sources fail."""
    fetcher = DataFetcher()
    sector_config = {"name": "Fintech", "companies": ["Paytm"]}
    
    async def mock_side_effect(label, *args, **kwargs):
        if "News" in label:
            return {"data": None, "status": "failed", "source_name": label}
        return {"data": "ok", "status": "ok", "source_name": label}

    with patch("data.scrapers._get_cached_or_fetch", side_effect=mock_side_effect) as mock_fetch:
        results = await fetcher.fetch_all(sector_config, ["Paytm"], "fake_news_key")
        
        assert results.health_score < 100
        assert results.health_score > 0

@pytest.mark.asyncio
async def test_retry_logic():
    """Test that fetch_with_retry actually retries on failure."""
    from data.scrapers import _fetch_with_retry
    
    mock_func = AsyncMock()
    mock_func.side_effect = [Exception("Fail"), Exception("Fail"), "Success"]
    
    res = await _fetch_with_retry(mock_func)
    assert res == "Success"
    assert mock_func.call_count == 3

@pytest.mark.asyncio
async def test_caching_logic():
    """Test that data is retrieved from cache if present."""
    from data.scrapers import cache
    
    sector_config = {"name": "CacheTest", "companies": ["Co"]}
    cache_key = "trends_CacheTest"
    mock_data = pd.DataFrame({"a": [1]})
    
    # Pre-populate cache
    from datetime import datetime
    cache.set(cache_key, (mock_data, datetime.now()))
    
    with patch("data.scrapers._fetch_with_retry") as mock_fetch:
        res = await _get_cached_or_fetch(
            "Trends", cache_key, 3600, MagicMock(), MagicMock(), ["Co"]
        )
        
        assert res["is_cached"] is True
        assert res["data"].equals(mock_data)
        mock_fetch.assert_not_called()
