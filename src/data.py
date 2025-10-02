# src/data.py
import os
import requests
from typing import Dict, Any, Optional

# New base (per Kalshi message) + legacy as fallback
BASES = [
    "https://api.elections.kalshi.com/trade-api/v2",  # new
    "https://trading-api.kalshi.com/v2",              # legacy v2
    "https://trading-api.kalshi.com/v1",              # legacy v1 (last resort)
]

KALSHI_API_KEY = os.getenv("KALSHI_API_KEY")
KALSHI_API_SECRET = os.getenv("KALSHI_API_SECRET")

def _make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    # Basic auth if user provides key+secret
    if KALSHI_API_KEY:
        s.auth = (KALSHI_API_KEY, KALSHI_API_SECRET or "")
    return s

def _get_json(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Try each base in order until one returns 200.
    Raise a helpful error otherwise.
    """
    sess = _make_session()
    last_err = None
    for base in BASES:
        url = f"{base.rstrip('/')}/{path.lstrip('/')}"
        try:
            r = sess.get(url, params=params, timeout=20)
            # Follow 301/302 manually just in case
            if r.is_redirect and r.headers.get("Location"):
                url = r.headers["Location"]
                r = sess.get(url, params=params, timeout=20)

            if r.status_code == 200:
                return r.json()

            # If unauthorized, explain what to do
            if r.status_code == 401:
                raise RuntimeError(
                    "401 Unauthorized from Kalshi. "
                    "Set KALSHI_API_KEY and KALSHI_API_SECRET in your environment "
                    "(and ensure they’re valid for the endpoint/venue). "
                    f"Response: {r.text}"
                )
            last_err = RuntimeError(f"{r.status_code} from {url} — {r.text[:300]}")
        except requests.RequestException as e:
            last_err = e
            continue
    # Nothing worked
    raise RuntimeError(f"All Kalshi bases failed. Last error: {last_err}")

def get_markets(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fetch list of markets. Some venues/endpoints may require auth.
    Example params you can try: {'venue': 'KX'} or pagination fields if documented.
    """
    return _get_json("/markets", params=params)

def get_market_by_ticker(ticker: str) -> Dict[str, Any]:
    """
    Fetch details of a single market by ticker.
    """
    return _get_json(f"/markets/{ticker}")

