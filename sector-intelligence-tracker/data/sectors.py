"""
data/sectors.py
---------------
Central configuration registry for all tracked sectors and companies.

Each sector entry declares:
- ``companies``       : ordered list of company display names
- ``app_ids``         : mapping of company name → Google Play Store app ID
- ``linkedin_slugs``  : mapping of company name → LinkedIn company slug
- ``insight``         : pre-written analyst narrative for the sector

This module contains **only configuration data** — no scraping logic.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Sector registry
# ---------------------------------------------------------------------------

SECTORS: dict[str, dict] = {
    "Fintech Payments": {
        "companies": ["Razorpay", "PhonePe", "Juspay", "BharatPe", "Simpl", "Scapia"],
        "app_ids": {
            "Razorpay": "com.razorpay.payments.app",
            "PhonePe": "com.phonepe.app",
            "Juspay": "in.juspay.hyperpay",
            "BharatPe": "com.bharatpe.app",
            "Simpl": "com.simpl.android",
            "Scapia": "com.scapia.app",
        },
        "linkedin_slugs": {
            "Razorpay": "razorpay",
            "PhonePe": "phonepe",
            "Juspay": "juspay",
            "BharatPe": "bharatpe",
            "Simpl": "simpl-buy-now-pay-later",
            "Scapia": "scapia",
        },
        "funding": {
            "Razorpay": {"last_round": "Series F", "amount_usd_m": 375, "year": 2021, "total_raised_usd_m": 816, "valuation_tier": "Unicorn"},
            "PhonePe": {"last_round": "Private Equity", "amount_usd_m": 850, "year": 2023, "total_raised_usd_m": 2200, "valuation_tier": "Unicorn"},
            "Juspay": {"last_round": "Series C", "amount_usd_m": 60, "year": 2021, "total_raised_usd_m": 87, "valuation_tier": "Soonicorn"},
            "BharatPe": {"last_round": "Series F", "amount_usd_m": 370, "year": 2021, "total_raised_usd_m": 680, "valuation_tier": "Unicorn"},
            "Simpl": {"last_round": "Series B", "amount_usd_m": 40, "year": 2021, "total_raised_usd_m": 83, "valuation_tier": "Growth"},
            "Scapia": {"last_round": "Series A", "amount_usd_m": 23, "year": 2023, "total_raised_usd_m": 32, "valuation_tier": "Growth"},
        },
        "insight": (
            "PhonePe leads on brand momentum and hiring velocity - a UPI scale play. "
            "Razorpay dominates B2B mindshare but lags on employer score, signalling "
            "rapid-scaling stress. Juspay is a quiet riser in news mentions."
        ),
    },
    "Analytics Consulting": {
        "companies": ["MathCo", "Sigmoid", "Tiger Analytics", "Fractal", "LatentView"],
        "app_ids": {},
        "linkedin_slugs": {
            "MathCo": "mathco",
            "Sigmoid": "sigmoid-analytics",
            "Tiger Analytics": "tiger-analytics",
            "Fractal": "fractal-analytics",
            "LatentView": "latentview-analytics",
        },
        "funding": {
            "MathCo": {"last_round": "Series A", "amount_usd_m": 50, "year": 2022, "total_raised_usd_m": 50, "valuation_tier": "Growth"},
            "Sigmoid": {"last_round": "Series B", "amount_usd_m": 12, "year": 2022, "total_raised_usd_m": 19, "valuation_tier": "Growth"},
            "Tiger Analytics": {"last_round": "Private Equity", "amount_usd_m": 40, "year": 2021, "total_raised_usd_m": 40, "valuation_tier": "Growth"},
            "Fractal": {"last_round": "Private Equity", "amount_usd_m": 360, "year": 2022, "total_raised_usd_m": 685, "valuation_tier": "Unicorn"},
            "LatentView": {"last_round": "IPO", "amount_usd_m": 80, "year": 2021, "total_raised_usd_m": 80, "valuation_tier": "Public"},
        },
        "insight": (
            "Fractal dominates news coverage and hiring - a global expansion signal. "
            "MathCo punches above its size on employer score. "
            "Tiger Analytics shows steady brand momentum."
        ),
    },
    "Wealthtech": {
        "companies": ["Smallcase", "Groww", "Zerodha", "Ditto", "INDmoney"],
        "app_ids": {
            "Smallcase": "com.smallcase.android",
            "Groww": "com.nextbillion.groww",
            "Zerodha": "com.zerodha.kite3",
            "Ditto": "in.ditto.app",
            "INDmoney": "com.indwealth.indmoney",
        },
        "linkedin_slugs": {
            "Smallcase": "smallcase",
            "Groww": "groww",
            "Zerodha": "zerodha",
            "Ditto": "ditto-insurance",
            "INDmoney": "indmoney",
        },
        "funding": {
            "Smallcase": {"last_round": "Series C", "amount_usd_m": 40, "year": 2021, "total_raised_usd_m": 65, "valuation_tier": "Soonicorn"},
            "Groww": {"last_round": "Series E", "amount_usd_m": 251, "year": 2021, "total_raised_usd_m": 393, "valuation_tier": "Unicorn"},
            "Zerodha": {"last_round": "Bootstrapped", "amount_usd_m": 0, "year": 2024, "total_raised_usd_m": 0, "valuation_tier": "Bootstrapped"},
            "Ditto": {"last_round": "Series A", "amount_usd_m": 4, "year": 2021, "total_raised_usd_m": 4, "valuation_tier": "Growth"},
            "INDmoney": {"last_round": "Series D", "amount_usd_m": 86, "year": 2022, "total_raised_usd_m": 144, "valuation_tier": "Soonicorn"},
        },
        "insight": (
            "Groww leads on both brand momentum and hiring - mass-market retail "
            "investing tailwinds. Zerodha holds the highest app rating despite zero "
            "paid marketing."
        ),
    },
    "Supply Chain Tech": {
        "companies": ["Zetwerk", "Ninjacart", "Locus", "Porter", "ElasticRun"],
        "app_ids": {
            "Porter": "in.porter.client",
            "Ninjacart": "com.ninjacart.app",
        },
        "linkedin_slugs": {
            "Zetwerk": "zetwerk",
            "Ninjacart": "ninjacart",
            "Locus": "locus-sh",
            "Porter": "porter-transport-solutions",
            "ElasticRun": "elasticrun",
        },
        "funding": {
            "Zetwerk": {"last_round": "Series F", "amount_usd_m": 120, "year": 2023, "total_raised_usd_m": 670, "valuation_tier": "Unicorn"},
            "Ninjacart": {"last_round": "Series D", "amount_usd_m": 145, "year": 2021, "total_raised_usd_m": 368, "valuation_tier": "Unicorn"},
            "Locus": {"last_round": "Series C", "amount_usd_m": 50, "year": 2021, "total_raised_usd_m": 80, "valuation_tier": "Soonicorn"},
            "Porter": {"last_round": "Series E", "amount_usd_m": 100, "year": 2021, "total_raised_usd_m": 130, "valuation_tier": "Soonicorn"},
            "ElasticRun": {"last_round": "Series E", "amount_usd_m": 330, "year": 2022, "total_raised_usd_m": 430, "valuation_tier": "Unicorn"},
        },
        "insight": (
            "Zetwerk is on a hiring blitz - manufacturing digitisation thesis playing "
            "out. Porter leads on app ratings. Locus quietly tops employer scores."
        ),
    },
    "Boutique Consulting": {
        "companies": ["Redseer", "Praxis", "Alvarez & Marsal", "Kroll", "Analysys Mason"],
        "app_ids": {},
        "linkedin_slugs": {
            "Redseer": "redseer-strategy-consultants",
            "Praxis": "praxis-global-alliance",
            "Alvarez & Marsal": "alvarezandmarsal",
            "Kroll": "kroll",
            "Analysys Mason": "analysys-mason",
        },
        "funding": {
            "Redseer": {"last_round": "Bootstrapped", "amount_usd_m": 0, "year": 2023, "total_raised_usd_m": 0, "valuation_tier": "Bootstrapped"},
            "Praxis": {"last_round": "Bootstrapped", "amount_usd_m": 0, "year": 2023, "total_raised_usd_m": 0, "valuation_tier": "Bootstrapped"},
            "Alvarez & Marsal": {"last_round": "Private", "amount_usd_m": 0, "year": 2024, "total_raised_usd_m": 0, "valuation_tier": "Private Enterprise"},
            "Kroll": {"last_round": "Private Equity", "amount_usd_m": 0, "year": 2024, "total_raised_usd_m": 0, "valuation_tier": "Private Enterprise"},
            "Analysys Mason": {"last_round": "Private", "amount_usd_m": 0, "year": 2024, "total_raised_usd_m": 0, "valuation_tier": "Private Enterprise"},
        },
        "insight": (
            "Redseer dominates brand search in India - strong content marketing "
            "flywheel. Alvarez and Marsal leads hiring. Kroll tops Glassdoor scores."
        ),
    },
}


# ---------------------------------------------------------------------------
# Helper accessors
# ---------------------------------------------------------------------------

def get_companies_for_sector(sector_key: str) -> list[str]:
    """
    Return the list of company names for a given sector key.

    Parameters
    ----------
    sector_key : str
        A key from :data:`SECTORS` (e.g. ``"Fintech Payments"``).

    Returns
    -------
    list[str]
        Ordered list of company display names.

    Raises
    ------
    KeyError
        If ``sector_key`` is not found in :data:`SECTORS`.
    """
    return SECTORS[sector_key]["companies"]


def get_company_by_slug(slug: str) -> dict | None:
    """
    Search all sectors and return the LinkedIn slug mapping entry matching ``slug``.

    Parameters
    ----------
    slug : str
        The URL-safe company identifier (e.g. ``"phonepe"``).

    Returns
    -------
    dict | None
        A dict ``{"company": name, "sector": sector_key}`` or ``None`` if not found.
    """
    for sector_key, sector in SECTORS.items():
        for company, company_slug in sector.get("linkedin_slugs", {}).items():
            if company_slug == slug:
                return {"company": company, "sector": sector_key}
    return None


def get_play_store_ids(sector_key: str) -> dict[str, str]:
    """
    Build a ``{company_name: play_store_id}`` mapping for a sector,
    filtering out companies where ``play_store_id`` is ``None``.

    Parameters
    ----------
    sector_key : str
        A key from :data:`SECTORS`.

    Returns
    -------
    dict[str, str]
        Mapping of company display names to their Play Store app IDs.
    """
    return {
        company: app_id
        for company, app_id in SECTORS[sector_key].get("app_ids", {}).items()
        if app_id
    }


def get_domains(sector_key: str) -> dict[str, str]:
    """
    Build a ``{company_name: domain}`` mapping for a sector,
    filtering out companies where ``domain`` is ``None``.

    Parameters
    ----------
    sector_key : str
        A key from :data:`SECTORS`.

    Returns
    -------
    dict[str, str]
        Mapping of company display names to root domains.
    """
    return {
        company: domain
        for company, domain in SECTORS[sector_key].get("domains", {}).items()
        if domain
    }


def get_trends_keywords(sector_key: str) -> list[str]:
    """
    Return an ordered list of Google Trends keywords for a sector.

    Uses the company display names as keywords (up to pytrends' 5-term limit).

    Parameters
    ----------
    sector_key : str
        A key from :data:`SECTORS`.

    Returns
    -------
    list[str]
        List of keyword strings, one per company, in config order.
    """
    return SECTORS[sector_key]["companies"][:5]


def list_sector_keys() -> list[str]:
    """
    Return all registered sector keys in insertion order.

    Returns
    -------
    list[str]
        List of sector key strings (e.g. ``["Fintech Payments", "Wealthtech", ...]``).
    """
    return list(SECTORS.keys())
