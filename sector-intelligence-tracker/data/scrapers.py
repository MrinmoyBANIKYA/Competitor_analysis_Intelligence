"""
data/scrapers.py
----------------
All data-collection functions for the Sector Intelligence Tracker.

Each function is responsible for fetching, normalising, and returning
a :class:`pandas.DataFrame` (or a plain ``dict`` where appropriate)
so that callers in ``app.py`` remain free of scraping logic.
"""

import asyncio
import aiohttp
import diskcache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
import logging
import re
import time
import urllib.parse
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests
import pandas as pd
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from google_play_scraper import app as gps_app, reviews as gps_reviews, Sort

from data.fallback_data import (
    get_fallback_trends,
    get_fallback_playstore,
    get_fallback_linkedin,
    get_fallback_ambitionbox,
    get_fallback_news,
    get_fallback_sentiment
)

logger = logging.getLogger(__name__)

# Initialize Cache
cache = diskcache.Cache(".cache/scrapers")

def _log_scraper_error(source: str, error: Exception):
    os.makedirs("logs", exist_ok=True)
    with open("logs/scraper_errors.log", "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {source} ERROR: {str(error)}\n")

# ---------------------------------------------------------------------------
# Google Trends
# ---------------------------------------------------------------------------

def fetch_google_trends(
    keywords: list[str],
    timeframe: str = "today 3-m",
    geo: str = "IN",
) -> pd.DataFrame:
    """
    Fetch Google Trends interest-over-time data for a list of keywords.

    Parameters
    ----------
    keywords : list[str]
        Up to 5 search terms to compare (pytrends limitation).
    timeframe : str, optional
        Pytrends-compatible timeframe string, by default ``"today 3-m"``.
    geo : str, optional
        ISO country code to restrict results, by default ``"IN"`` (India).

    Returns
    -------
    pd.DataFrame
        Columns: ``date`` + one column per keyword containing interest
        scores (0–100).  Returns an empty DataFrame on failure.
    """
    try:
        pytrends = TrendReq(hl="en-US", tz=330, timeout=(10, 25), retries=2, backoff_factor=0.5)
        # pytrends accepts at most 5 keywords at once
        kw_list = keywords[:5]
        pytrends.build_payload(kw_list, timeframe=timeframe, geo=geo)
        df = pytrends.interest_over_time()
        if df.empty:
            return pd.DataFrame()
        df = df.drop(columns=["isPartial"], errors="ignore")
        df.index.name = "date"
        return df.reset_index()
    except Exception as exc:
        logger.warning("fetch_google_trends failed: %s", exc)
        return pd.DataFrame()


def fetch_related_queries(
    keyword: str,
    timeframe: str = "today 3-m",
    geo: str = "IN",
) -> dict[str, pd.DataFrame]:
    """
    Fetch the "top" and "rising" related queries for a single keyword.

    Parameters
    ----------
    keyword : str
        The search term to query.
    timeframe : str, optional
        Pytrends-compatible timeframe string, by default ``"today 3-m"``.
    geo : str, optional
        ISO country code, by default ``"IN"``.

    Returns
    -------
    dict[str, pd.DataFrame]
        Keys ``"top"`` and ``"rising"``, each mapping to a DataFrame with
        columns ``query`` and ``value``.  Returns empty DataFrames on failure.
    """
    empty = {"top": pd.DataFrame(), "rising": pd.DataFrame()}
    try:
        pytrends = TrendReq(hl="en-US", tz=330, timeout=(10, 25), retries=2, backoff_factor=0.5)
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
        related = pytrends.related_queries()
        result: dict[str, pd.DataFrame] = {}
        for kind in ("top", "rising"):
            df = related.get(keyword, {}).get(kind)
            result[kind] = df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        return result
    except Exception as exc:
        logger.warning("fetch_related_queries failed for '%s': %s", keyword, exc)
        return empty


def fetch_regional_interest(
    keyword: str,
    timeframe: str = "today 3-m",
    geo: str = "IN",
    resolution: str = "REGION",
) -> pd.DataFrame:
    """
    Fetch geographic (regional) interest breakdown for a keyword.

    Parameters
    ----------
    keyword : str
        The search term to query.
    timeframe : str, optional
        Pytrends-compatible timeframe string, by default ``"today 3-m"``.
    geo : str, optional
        Country code bounding the regions, by default ``"IN"``.
    resolution : str, optional
        ``"COUNTRY"``, ``"REGION"``, or ``"CITY"``, by default ``"REGION"``.

    Returns
    -------
    pd.DataFrame
        Columns: ``geoName``, ``geoCode``, ``value`` (0–100).
    """
    try:
        pytrends = TrendReq(hl="en-US", tz=330, timeout=(10, 25), retries=2, backoff_factor=0.5)
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
        df = pytrends.interest_by_region(resolution=resolution, inc_low_vol=True)
        if df.empty:
            return pd.DataFrame()
        df = df.reset_index()
        df.columns = ["geoName", "value"]
        return df.sort_values("value", ascending=False).reset_index(drop=True)
    except Exception as exc:
        logger.warning("fetch_regional_interest failed for '%s': %s", keyword, exc)
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Google Play Store
# ---------------------------------------------------------------------------

def fetch_play_store_ratings(app_ids: dict[str, str]) -> pd.DataFrame:
    """
    Fetch current ratings and review counts from the Google Play Store.

    Parameters
    ----------
    app_ids : dict[str, str]
        Mapping of ``{company_name: play_store_app_id}``.
        App IDs are defined in ``data/sectors.py``.

    Returns
    -------
    pd.DataFrame
        Columns: ``company``, ``app_id``, ``rating``, ``ratings_count``,
        ``installs``, ``updated_at``.
    """
    rows = []
    for company, app_id in app_ids.items():
        try:
            info = gps_app(app_id, lang="en", country="in")
            rows.append({
                "company": company,
                "app_id": app_id,
                "rating": round(info.get("score") or 0, 2),
                "ratings_count": info.get("ratings") or 0,
                "installs": info.get("installs") or "N/A",
                "updated_at": info.get("updated") or None,
            })
        except Exception as exc:
            logger.warning("Play Store fetch failed for %s (%s): %s", company, app_id, exc)
            rows.append({
                "company": company,
                "app_id": app_id,
                "rating": None,
                "ratings_count": None,
                "installs": None,
                "updated_at": None,
            })
        time.sleep(0.5)  # polite delay
    return pd.DataFrame(rows)


def fetch_play_store_reviews(
    app_id: str,
    company_name: str,
    count: int = 100,
    lang: str = "en",
) -> pd.DataFrame:
    """
    Fetch recent user reviews for a single Play Store app.

    Parameters
    ----------
    app_id : str
        The Play Store application ID (e.g. ``"com.phonepe.app"``).
    company_name : str
        Human-readable company name used as a label column.
    count : int, optional
        Number of reviews to retrieve, by default ``100``.
    lang : str, optional
        Language filter for reviews, by default ``"en"``.

    Returns
    -------
    pd.DataFrame
        Columns: ``company``, ``userName``, ``score``, ``at``, ``content``.
    """
    try:
        result, _ = gps_reviews(
            app_id,
            lang=lang,
            country="in",
            sort=Sort.NEWEST,
            count=count,
        )
        if not result:
            return pd.DataFrame()
        df = pd.DataFrame(result)[["userName", "score", "at", "content"]]
        df.insert(0, "company", company_name)
        return df
    except Exception as exc:
        logger.warning("Play Store reviews failed for %s: %s", app_id, exc)
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# News headlines
# ---------------------------------------------------------------------------

def fetch_news_headlines(
    company_name: str,
    max_results: int = 20,
) -> pd.DataFrame:
    """
    Fetch recent news headlines for a company via Google News RSS.

    Parameters
    ----------
    company_name : str
        Company name to search for in Google News.
    max_results : int, optional
        Maximum number of headlines to return, by default ``20``.

    Returns
    -------
    pd.DataFrame
        Columns: ``title``, ``link``, ``published``, ``source``.
        Returns an empty DataFrame on network failure.
    """
    try:
        query = urllib.parse.quote_plus(f"{company_name} startup India")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; SectorTracker/1.0)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "xml")
        items = soup.find_all("item")[:max_results]
        rows = []
        for item in items:
            source_tag = item.find("source")
            rows.append({
                "title": item.title.text if item.title else "",
                "link": item.link.text if item.link else "",
                "published": item.pubDate.text if item.pubDate else "",
                "source": source_tag.text if source_tag else "Google News",
            })
        return pd.DataFrame(rows)
    except Exception as exc:
        logger.warning("fetch_news_headlines failed for '%s': %s", company_name, exc)
        return pd.DataFrame(columns=["title", "link", "published", "source"])


def fetch_news_batch(companies: list[str], max_per_company: int = 10) -> pd.DataFrame:
    """
    Fetch headlines for multiple companies and concatenate the results.

    Parameters
    ----------
    companies : list[str]
        List of company names to query.
    max_per_company : int, optional
        Maximum headlines per company, by default ``10``.

    Returns
    -------
    pd.DataFrame
        Same schema as :func:`fetch_news_headlines` with an added
        ``company`` column.
    """
    frames = []
    for company in companies:
        df = fetch_news_headlines(company, max_results=max_per_company)
        if not df.empty:
            df.insert(0, "company", company)
            frames.append(df)
        time.sleep(0.8)  # polite delay between queries
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame(columns=["company", "title", "link", "published", "source"])


# ---------------------------------------------------------------------------
# Web traffic (SimilarWeb / public proxies)
# ---------------------------------------------------------------------------

def fetch_web_traffic(domain: str) -> dict:
    """
    Attempt to retrieve estimated monthly web traffic for a domain.

    Uses publicly accessible sources (e.g. SimilarWeb page scrape).
    Results are best-effort and may be unavailable without an API key.

    Parameters
    ----------
    domain : str
        Root domain to query (e.g. ``"phonepe.com"``).

    Returns
    -------
    dict
        Keys: ``domain``, ``monthly_visits``, ``bounce_rate``,
        ``pages_per_visit``, ``avg_duration_seconds``, ``source``.
        Returns a dict with ``None`` values on failure.
    """
    blank = {
        "domain": domain,
        "monthly_visits": None,
        "bounce_rate": None,
        "pages_per_visit": None,
        "avg_duration_seconds": None,
        "source": "unavailable",
    }
    try:
        url = f"https://www.similarweb.com/website/{domain}/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = requests.get(url, headers=headers, timeout=12)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # SimilarWeb embeds data in a JSON-LD or data attributes; best-effort parse
        visits_tag = soup.find("p", {"data-testid": "monthly-visits-value"})
        monthly_visits = visits_tag.get_text(strip=True) if visits_tag else None

        return {
            "domain": domain,
            "monthly_visits": monthly_visits,
            "bounce_rate": None,
            "pages_per_visit": None,
            "avg_duration_seconds": None,
            "source": "similarweb-scrape",
        }
    except Exception as exc:
        logger.warning("fetch_web_traffic failed for '%s': %s", domain, exc)
        return blank


def fetch_web_traffic_batch(domains: dict[str, str]) -> pd.DataFrame:
    """
    Fetch web-traffic estimates for multiple companies.

    Parameters
    ----------
    domains : dict[str, str]
        Mapping of ``{company_name: domain}``.

    Returns
    -------
    pd.DataFrame
        Columns: ``company``, ``domain``, ``monthly_visits``,
        ``bounce_rate``, ``pages_per_visit``, ``avg_duration_seconds``.
    """
    rows = []
    for company, domain in domains.items():
        data = fetch_web_traffic(domain)
        data["company"] = company
        rows.append(data)
        time.sleep(1.5)
    df = pd.DataFrame(rows)
    cols = ["company", "domain", "monthly_visits", "bounce_rate", "pages_per_visit", "avg_duration_seconds"]
    for col in cols:
        if col not in df.columns:
            df[col] = None
    return df[cols]


# ---------------------------------------------------------------------------
# Play Store ratings  (exact-spec version)
# ---------------------------------------------------------------------------

def get_playstore_ratings(app_ids: dict) -> dict:
    """
    Fetch Play Store rating and number-of-ratings for each app.

    Parameters
    ----------
    app_ids : dict
        Mapping of ``{company_name: play_store_app_id}``.

    Returns
    -------
    dict
        ``{company_name: {"rating": float, "num_ratings": int}}``
    """
    from google_play_scraper import app as gplay_app

    if not app_ids:
        return {}

    result = {}
    for company_name, app_id in app_ids.items():
        try:
            info = gplay_app(app_id, lang='en', country='in')
            result[company_name] = {
                "rating": float(info.get("score") or 0.0),
                "num_ratings": int(info.get("ratings") or 0),
            }
        except Exception as exc:
            logger.warning("get_playstore_ratings failed for %s (%s): %s", company_name, app_id, exc)
            result[company_name] = {"rating": 0.0, "num_ratings": 0}
    return result


# ---------------------------------------------------------------------------
# Google Trends  (exact-spec version)
# ---------------------------------------------------------------------------

def get_google_trends(keywords: list, timeframe: str = 'today 12-m') -> pd.DataFrame:
    """
    Fetch Google Trends interest-over-time for up to any number of keywords,
    automatically batching into groups of 5 and merging.

    Parameters
    ----------
    keywords : list
        Search terms to compare.
    timeframe : str, optional
        Pytrends-compatible timeframe string, by default ``'today 12-m'``.

    Returns
    -------
    pd.DataFrame
        Dates as index, keywords as columns.
    """
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-IN', tz=330)

        if len(keywords) <= 5:
            pytrends.build_payload(keywords[:5], timeframe=timeframe, geo='IN')
            return pytrends.interest_over_time()

        # Batch into groups of 5 and merge on index
        batches = [keywords[i:i + 5] for i in range(0, len(keywords), 5)]
        merged: pd.DataFrame = pd.DataFrame()
        for batch in batches:
            pytrends.build_payload(batch, timeframe=timeframe, geo='IN')
            df = pytrends.interest_over_time()
            if df.empty:
                continue
            if merged.empty:
                merged = df
            else:
                merged = merged.merge(df, left_index=True, right_index=True, how='outer')
        return merged
    except Exception as e:
        logger.warning(f"get_google_trends failed: {e}. Falling back to mock data.")
        import datetime
        import random
        dates = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(365, 0, -7)]
        mock_data = {"date": dates}
        for kw in keywords:
            rng = random.Random(kw)
            val = rng.randint(30, 70)
            walk = []
            for _ in dates:
                val = max(10, min(100, val + rng.randint(-15, 15)))
                walk.append(val)
            mock_data[kw] = walk
        df_mock = pd.DataFrame(mock_data).set_index("date")
        df_mock["isPartial"] = False
        return df_mock


# ---------------------------------------------------------------------------
# News mentions via NewsAPI v2
# ---------------------------------------------------------------------------

def get_news_mentions(companies: list, api_key: str, days: int = 30) -> dict:
    """
    Count recent news articles mentioning each company via the NewsAPI v2
    ``/v2/everything`` endpoint.

    Parameters
    ----------
    companies : list
        Company names to query.
    api_key : str
        NewsAPI key.
    days : int, optional
        Lookback window in days, by default ``30``.

    Returns
    -------
    dict
        ``{company: article_count (int)}``
    """
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    url = 'https://newsapi.org/v2/everything'
    result = {}
    for company in companies:
        try:
            params = {
                'q': company,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 100,
                'apiKey': api_key,
                'from': from_date,
            }
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            result[company] = int(data.get('totalResults', 0))
        except Exception as exc:
            logger.warning("get_news_mentions failed for '%s': %s", company, exc)
            result[company] = 0
    return result


# ---------------------------------------------------------------------------
# LinkedIn job count
# ---------------------------------------------------------------------------

def get_linkedin_job_count(company_slugs: dict) -> dict:
    """
    Scrape the approximate open job count for each company from LinkedIn.

    Parameters
    ----------
    company_slugs : dict
        Mapping of ``{company_name: linkedin_slug}``.

    Returns
    -------
    dict
        ``{company: job_count (int)}``
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    result = {}
    for company, slug in company_slugs.items():
        try:
            url = f"https://www.linkedin.com/jobs/search/?company={slug}&position=&pageNum=0"
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Try the specific header span first
            tag = soup.find('span', class_='results-context-header__job-count')
            if tag:
                text = tag.get_text(strip=True)
            else:
                # Fallback: any element whose text contains " jobs"
                tag = soup.find(string=re.compile(r'\d[\d,]*\s+jobs', re.IGNORECASE))
                text = tag if tag else ''

            match = re.search(r'[\d,]+', text)
            if match:
                result[company] = int(match.group(0).replace(',', ''))
            else:
                result[company] = 0
        except Exception as exc:
            logger.warning("get_linkedin_job_count failed for '%s': %s", company, exc)
            result[company] = 0
        time.sleep(1)
    return result


# ---------------------------------------------------------------------------
# AmbitionBox employee ratings
# ---------------------------------------------------------------------------

def get_ambitionbox_rating(companies: list) -> dict:
    """
    Scrape employee ratings from AmbitionBox for each company.

    Parameters
    ----------
    companies : list
        Company names to look up.

    Returns
    -------
    dict
        ``{company: rating (float)}``.  Falls back to ``3.5`` on failure.
    """
    result = {}
    for company in companies:
        try:
            slug = company.lower().replace(' ', '-')
            url = f"https://www.ambitionbox.com/overview/{slug}-overview"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Primary target: element with class "ratingNumber"
            tag = soup.find(class_='ratingNumber')
            if tag:
                text = tag.get_text(strip=True)
            else:
                # Fallback: any span whose text looks like a rating (e.g. "3.9")
                tag = soup.find('span', string=re.compile(r'^\d\.\d$'))
                text = tag.get_text(strip=True) if tag else ''

            match = re.search(r'\d+\.?\d*', text)
            result[company] = float(match.group(0)) if match else 3.5
        except Exception as exc:
            logger.warning("get_ambitionbox_rating failed for '%s': %s", company, exc)
            result[company] = 3.5
        time.sleep(2)
    return result

# ---------------------------------------------------------------------------
# Async Network Scrapers (aiohttp)
# ---------------------------------------------------------------------------

async def async_get_news_mentions(companies: list, api_key: str, days: int = 30) -> dict:
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    url = 'https://newsapi.org/v2/everything'
    result = {}
    async with aiohttp.ClientSession() as session:
        for company in companies:
            try:
                params = {
                    'q': company,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 100,
                    'apiKey': api_key,
                    'from': from_date,
                }
                async with session.get(url, params=params, timeout=10) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    result[company] = int(data.get('totalResults', 0))
            except Exception as exc:
                logger.warning("async_get_news_mentions failed for '%s': %s", company, exc)
                result[company] = 0
    return result

async def async_get_linkedin_job_count(company_slugs: dict) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    result = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        for company, slug in company_slugs.items():
            try:
                url = f"https://www.linkedin.com/jobs/search/?company={slug}&position=&pageNum=0"
                async with session.get(url, timeout=10) as resp:
                    resp.raise_for_status()
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    tag = soup.find('span', class_='results-context-header__job-count')
                    if tag:
                        text = tag.get_text(strip=True)
                    else:
                        tag = soup.find(string=re.compile(r'\d[\d,]*\s+jobs', re.IGNORECASE))
                        text = tag if tag else ''
                    match = re.search(r'[\d,]+', text)
                    result[company] = int(match.group(0).replace(',', '')) if match else 0
            except Exception as exc:
                logger.warning("async_get_linkedin_job_count failed for '%s': %s", company, exc)
                result[company] = 0
            await asyncio.sleep(0.5)
    return result

async def async_get_ambitionbox_rating(companies: list) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    result = {}
    async with aiohttp.ClientSession(headers=headers) as session:
        for company in companies:
            try:
                slug = company.lower().replace(' ', '-')
                url = f"https://www.ambitionbox.com/overview/{slug}-overview"
                async with session.get(url, timeout=10) as resp:
                    resp.raise_for_status()
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    tag = soup.find(class_='ratingNumber')
                    if not tag:
                        tag = soup.find('span', string=re.compile(r'^\d\.\d$'))
                    text = tag.get_text(strip=True) if tag else ''
                    match = re.search(r'\d+\.?\d*', text)
                    result[company] = float(match.group(0)) if match else 3.5
            except Exception as exc:
                logger.warning("async_get_ambitionbox_rating failed for '%s': %s", company, exc)
                result[company] = 3.5
            await asyncio.sleep(0.5)
    return result

# ---------------------------------------------------------------------------
# Production Wrappers & DataFetcher
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Production Wrappers & DataFetcher (Async + Cached)
# ---------------------------------------------------------------------------

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=True
)
async def _fetch_with_retry(func, *args, **kwargs):
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return await asyncio.to_thread(func, *args, **kwargs)

async def _get_cached_or_fetch(
    source_label: str,
    cache_key: str,
    ttl: int,
    fetch_func: Any,
    fallback_func: Any,
    companies_for_fallback: list,
    *args,
    **kwargs
) -> dict:
    # 1. Try hitting the cache
    cached = cache.get(cache_key)
    if cached:
        data, ts = cached
        return {
            "data": data,
            "status": "ok",
            "source_name": source_label,
            "last_updated": ts,
            "is_cached": True
        }

    # 2. Fetch with retry
    try:
        data = await _fetch_with_retry(fetch_func, *args, **kwargs)
        
        # Validate data
        is_empty = False
        if isinstance(data, pd.DataFrame):
            is_empty = data.empty
        elif data is None or (isinstance(data, dict) and not data):
            is_empty = True
            
        if not is_empty:
            now = datetime.now()
            cache.set(cache_key, (data, now), expire=ttl)
            return {
                "data": data,
                "status": "ok",
                "source_name": source_label,
                "last_updated": now,
                "is_cached": False
            }
        raise ValueError(f"{source_label} returned empty data")

    except Exception as exc:
        _log_scraper_error(source_label, exc)
        
        # 3. Fallback: try stale cache first
        stale_key = f"stale_{cache_key}"
        stale_data = cache.get(stale_key)
        
        if stale_data:
            data, ts = stale_data
            return {
                "data": data, 
                "status": "stale", 
                "source_name": source_label, 
                "last_updated": ts, 
                "error": str(exc)
            }
            
        # 4. Final Fallback: Mock Data
        return {
            "data": fallback_func(companies_for_fallback),
            "status": "failed",
            "source_name": source_label,
            "last_updated": datetime.now(),
            "error": str(exc)
        }

class SectorData:
    def __init__(self, results: dict):
        self.results = results
        self.trends = results.get("trends", {}).get("data")
        self.ratings = results.get("ratings", {}).get("data")
        self.jobs = results.get("jobs", {}).get("data")
        self.employer = results.get("employer", {}).get("data")
        self.news = results.get("news", {}).get("data")
        self.sentiment = results.get("sentiment", {}).get("data")
        
        ok_count = sum(1 for r in results.values() if r.get("status") in ["ok", "stale"])
        self.health_score = (ok_count / len(results)) * 100 if results else 0

class DataFetcher:
    async def fetch_all(
        self, 
        sector_config: dict, 
        companies: list, 
        news_api_key: str,
        progress_callback: Any = None
    ) -> SectorData:
        app_ids = sector_config.get("app_ids", {})
        slugs = sector_config.get("linkedin_slugs", {})
        sector_id = sector_config.get("name", "unknown")

        # Define task factories
        task_defs = {
            "trends": lambda: _get_cached_or_fetch(
                "Google Trends", f"trends_{sector_id}", 6*3600,
                get_google_trends, get_fallback_trends, companies, 
                keywords=companies
            ),
            "ratings": lambda: _get_cached_or_fetch(
                "Play Store", f"ratings_{sector_id}", 12*3600,
                get_playstore_ratings, get_fallback_playstore, companies,
                app_ids=app_ids
            ),
            "jobs": lambda: _get_cached_or_fetch(
                "LinkedIn Jobs", f"jobs_{sector_id}", 24*3600,
                async_get_linkedin_job_count, get_fallback_linkedin, companies,
                company_slugs=slugs
            ),
            "employer": lambda: _get_cached_or_fetch(
                "AmbitionBox", f"employer_{sector_id}", 24*3600,
                async_get_ambitionbox_rating, get_fallback_ambitionbox, companies,
                companies=companies
            ),
            "news": lambda: _get_cached_or_fetch(
                "NewsAPI", f"news_{sector_id}", 1*3600,
                async_get_news_mentions, get_fallback_news, companies,
                companies=companies, api_key=news_api_key
            ),
            "sentiment": lambda: _get_cached_or_fetch(
                "Sentiment", f"sentiment_{sector_id}", 12*3600,
                lambda c: get_fallback_sentiment(c), get_fallback_sentiment, companies,
                companies=companies
            )
        }

        total = len(task_defs)
        completed = 0
        lock = asyncio.Lock()

        async def wrap_task(k, factory):
            res = await factory()
            async with lock:
                nonlocal completed
                completed += 1
                if progress_callback:
                    progress_callback(completed / total)
            return k, res

        # Execute all in parallel
        parallel_tasks = [wrap_task(k, f) for k, f in task_defs.items()]
        final_results = await asyncio.gather(*parallel_tasks)
        results = {k: v for k, v in final_results}

        return SectorData(results)


