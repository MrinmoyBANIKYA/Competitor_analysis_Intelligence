"""
utils/helpers.py
----------------
Shared utility functions for the Sector Intelligence Tracker.

These helpers are intentionally free of Streamlit or scraping imports
so they can be unit-tested independently.
"""

from __future__ import annotations

import datetime
import re
import time
import functools
import logging
from typing import Any, Callable

import pandas as pd


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_large_number(value: int | float, precision: int = 1) -> str:
    """
    Format a large integer or float into a human-readable abbreviation.

    Examples
    --------
    >>> format_large_number(1_500_000)
    '1.5M'
    >>> format_large_number(23_400)
    '23.4K'

    Parameters
    ----------
    value : int | float
        The numeric value to format.
    precision : int, optional
        Decimal places in the abbreviated form, by default ``1``.

    Returns
    -------
    str
        Abbreviated string such as ``"1.5M"``, ``"23.4K"``, or ``"999"``.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.{precision}f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{precision}f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.{precision}f}K"
    return f"{value:.0f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a float as a percentage string.

    Parameters
    ----------
    value : float
        A ratio between 0 and 1  (e.g. ``0.42`` → ``"42.0%"``),
        or an already-scaled percentage (e.g. ``42.0`` → ``"42.0%"``).
        Values > 1 are treated as already-scaled.
    decimals : int, optional
        Number of decimal places, by default ``1``.

    Returns
    -------
    str
        Percentage string, e.g. ``"42.0%"``.
    """
    if value <= 1.0:
        value = value * 100
    return f"{value:.{decimals}f}%"


def format_duration(seconds: int | float) -> str:
    """
    Convert a duration in seconds to a human-readable string.

    Parameters
    ----------
    seconds : int | float
        Duration in seconds.

    Returns
    -------
    str
        Formatted string such as ``"3m 24s"`` or ``"1h 02m"``.
    """
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    if minutes:
        return f"{minutes}m {secs:02d}s"
    return f"{secs}s"


def timestamp_label(fmt: str = "%d %b %Y, %H:%M") -> str:
    """
    Return the current local datetime formatted as a display label.

    Parameters
    ----------
    fmt : str, optional
        ``strftime`` format string, by default ``"%d %b %Y, %H:%M"``.

    Returns
    -------
    str
        Formatted datetime string, e.g. ``"07 Apr 2025, 14:32"``.
    """
    return datetime.datetime.now().strftime(fmt)


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def safe_get(d: dict, *keys: str, default: Any = None) -> Any:
    """
    Safely retrieve a deeply nested value from a dict without raising.

    Parameters
    ----------
    d : dict
        The source dictionary.
    *keys : str
        An ordered sequence of keys forming the lookup path.
    default : Any, optional
        Fallback value returned when any key is missing, by default ``None``.

    Returns
    -------
    Any
        The nested value if all keys exist, otherwise ``default``.
    """
    current = d
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply generic cleaning steps to a raw DataFrame.

    Steps applied:
    1. Strip leading/trailing whitespace from all string columns.
    2. Drop fully-duplicate rows.
    3. Reset the index.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame to clean.

    Returns
    -------
    pd.DataFrame
        Cleaned copy.  The original is not mutated.
    """
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def pivot_trends(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """
    Pivot a tidy interest-over-time DataFrame into wide format.

    Expects a DataFrame with columns ``[date, keyword, value]`` and
    returns one where each keyword becomes its own column.

    Parameters
    ----------
    df : pd.DataFrame
        Tidy trends DataFrame.
    date_col : str, optional
        Name of the date column, by default ``"date"``.

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame indexed by date.
    """
    if df.empty:
        return df
    return df.pivot(index=date_col, columns="keyword", values="value")


def sentiment_label(score: float) -> str:
    """
    Convert a numeric sentiment score to a human-readable label.

    Parameters
    ----------
    score : float
        Sentiment polarity in the range ``[-1.0, 1.0]``  (or 1–5 star scale).

    Returns
    -------
    str
        One of ``"Positive"``, ``"Neutral"``, or ``"Negative"``.
    """
    if score > 0.1:
        return "Positive"
    if score < -0.1:
        return "Negative"
    return "Neutral"


# ---------------------------------------------------------------------------
# Colour / visual helpers
# ---------------------------------------------------------------------------

_PALETTES: dict[str, list[str]] = {
    "teal":   ["#00897B", "#26A69A", "#4DB6AC", "#80CBC4", "#B2DFDB"],
    "orange": ["#E65100", "#F57C00", "#FB8C00", "#FFA726", "#FFCC80"],
    "purple": ["#4527A0", "#5E35B1", "#7E57C2", "#9575CD", "#B39DDB"],
    "green":  ["#1B5E20", "#2E7D32", "#388E3C", "#43A047", "#66BB6A"],
    "blue":   ["#0D47A1", "#1565C0", "#1976D2", "#1E88E5", "#42A5F5"],
}


def get_color_scale(n: int, palette: str = "teal") -> list[str]:
    """
    Generate a list of ``n`` hex colour strings from a named palette.

    Parameters
    ----------
    n : int
        Number of colours to generate.
    palette : str, optional
        Named palette key.  Supported values: ``"teal"``, ``"orange"``,
        ``"purple"``, ``"green"``.  Defaults to ``"teal"``.

    Returns
    -------
    list[str]
        List of hex colour strings (e.g. ``["#00897B", "#26A69A", ...]``).
    """
    colors = _PALETTES.get(palette, _PALETTES["teal"])
    if n <= len(colors):
        return colors[:n]
    # Repeat / cycle if more colours needed
    return [colors[i % len(colors)] for i in range(n)]


# ---------------------------------------------------------------------------
# Caching / retry helpers
# ---------------------------------------------------------------------------

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,),
) -> Callable:
    """
    Decorator that retries the wrapped function on specified exceptions.

    Parameters
    ----------
    max_attempts : int, optional
        Total number of attempts before re-raising, by default ``3``.
    delay : float, optional
        Seconds to wait between attempts, by default ``1.0``.
    exceptions : tuple, optional
        Exception types that trigger a retry, by default ``(Exception,)``.

    Returns
    -------
    Callable
        Decorated function with built-in retry logic.
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    logger.warning(
                        "Attempt %d/%d for %s failed: %s",
                        attempt, max_attempts, fn.__name__, exc,
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc  # type: ignore[misc]
        return wrapper
    return decorator


def throttle(calls_per_second: float = 1.0) -> Callable:
    """
    Decorator that enforces a minimum interval between calls.

    Useful for rate-limited APIs such as pytrends.

    Parameters
    ----------
    calls_per_second : float, optional
        Maximum call rate, by default ``1.0``.

    Returns
    -------
    Callable
        Decorated function that sleeps if called too quickly.
    """
    min_interval = 1.0 / calls_per_second

    def decorator(fn: Callable) -> Callable:
        last_called: list[float] = [0.0]

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            elapsed = time.monotonic() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = fn(*args, **kwargs)
            last_called[0] = time.monotonic()
            return result
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# URL / string helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """
    Convert an arbitrary string to a URL-safe slug.

    Parameters
    ----------
    text : str
        Input string (e.g. ``"PhonePe Payments"``).

    Returns
    -------
    str
        Lowercase hyphen-separated slug (e.g. ``"phonepe-payments"``).
    """
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = text.strip("-")
    return text


def truncate(text: str, max_len: int = 80, ellipsis: str = "…") -> str:
    """
    Truncate a string to ``max_len`` characters, appending an ellipsis.

    Parameters
    ----------
    text : str
        Input string.
    max_len : int, optional
        Maximum character count including the ellipsis, by default ``80``.
    ellipsis : str, optional
        String appended when truncation occurs, by default ``"…"``.

    Returns
    -------
    str
        Truncated string, or the original if it fits within ``max_len``.
    """
    if len(text) <= max_len:
        return text
    return text[: max_len - len(ellipsis)] + ellipsis
