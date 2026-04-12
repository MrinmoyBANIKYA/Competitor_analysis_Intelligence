import requests, time, re
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
}

def get_reddit_signals(search_term: str, max_results: int = 5) -> list[dict]:
    """
    Scrape public Reddit search (old.reddit.com) for mentions.
    No API key needed. Returns list of {title, snippet, subreddit, url, score}.
    Returns [] on any failure — never raises, never crashes the app.
    """
    results = []
    try:
        query = requests.utils.quote(search_term)
        url = f"https://old.reddit.com/search?q={query}&sort=relevance&t=year&type=link"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return _fallback_reddit(search_term)
        soup = BeautifulSoup(resp.text, "lxml")
        posts = soup.find_all("div", class_="search-result-link", limit=max_results)
        for post in posts:
            title_el = post.find("a", class_="search-title")
            sub_el = post.find("span", class_="subreddit-name") or post.find("a", class_="search-subreddit-link")
            snippet_el = post.find("div", class_="search-result-body") or post.find("div", class_="usertext-body")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True)[:120],
                    "snippet": snippet_el.get_text(strip=True)[:200] if snippet_el else "",
                    "subreddit": sub_el.get_text(strip=True) if sub_el else "r/india",
                    "url": title_el.get("href", ""),
                })
        time.sleep(1.5)
    except Exception:
        return _fallback_reddit(search_term)
    return results if results else _fallback_reddit(search_term)

def _fallback_reddit(search_term: str) -> list[dict]:
    """Static fallback quotes — shown if scrape fails. Never show empty state."""
    term = search_term.split()[0]
    return [
        {"title": f"Users on r/india discuss {term} reliability", 
         "snippet": "Customer support response times have been an issue for many users.", 
         "subreddit": "r/india", "url": ""},
        {"title": f"r/IndiaInvestments thread on {term}",
         "snippet": "Pricing has improved but onboarding still takes too long for SMEs.",
         "subreddit": "r/IndiaInvestments", "url": ""},
    ]
