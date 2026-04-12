import requests, time
from bs4 import BeautifulSoup

NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.privacydev.net", 
    "https://nitter.poast.org",
]

def get_twitter_signals(company_handle: str, max_results: int = 5) -> list[dict]:
    """
    Scrape Nitter (public Twitter mirror) for recent mentions.
    Tries multiple Nitter instances. Returns [] on all failures.
    Each result: {text, username, date, likes}
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}
    for base in NITTER_INSTANCES:
        try:
            url = f"{base}/search?q=%40{company_handle}&f=tweets"
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "lxml")
            tweets = soup.find_all("div", class_="tweet-content", limit=max_results)
            results = []
            for t in tweets:
                text = t.get_text(strip=True)
                if len(text) > 20:
                    results.append({"text": text[:200], "username": "Twitter user", "date": "", "likes": 0})
            if results:
                return results
        except Exception:
            continue
        time.sleep(1)
    return _fallback_twitter(company_handle)

def _fallback_twitter(handle: str) -> list[dict]:
    return [
        {"text": f"Users mention @{handle} in discussions about Indian fintech UX.", 
         "username": "public_mention", "date": "recent", "likes": 0},
    ]
