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
        "insight": (
            "PhonePe leads on brand momentum and hiring velocity — a UPI scale play. "
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
        "insight": (
            "Fractal dominates news coverage and hiring — a global expansion signal. "
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
        "insight": (
            "Groww leads on both brand momentum and hiring — mass-market retail "
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
        "insight": (
            "Zetwerk is on a hiring blitz — manufacturing digitisation thesis playing "
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
        "insight": (
            "Redseer dominates brand search in India — strong content marketing "
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
