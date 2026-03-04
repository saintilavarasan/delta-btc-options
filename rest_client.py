"""
REST Client for Delta Exchange BTC Options
Includes error handling, retries, and logging
"""

import requests
import time
import logging
from typing import List, Dict, Optional
from config import (
    DELTA_REST_PRODUCTS_URL,
    DELTA_REST_TICKERS_URL,
    REST_TIMEOUT,
    REST_RETRY_ATTEMPTS,
    REST_RETRY_BACKOFF,
    REST_RETRY_MAX_WAIT,
    CONTRACT_TYPES,
)

logger = logging.getLogger(__name__)

HEADERS = {"Accept": "application/json"}


def _exponential_backoff(attempt: int) -> float:
    """Calculate exponential backoff"""
    wait = min(REST_RETRY_BACKOFF ** attempt, REST_RETRY_MAX_WAIT)
    return wait


def load_options_from_rest() -> List[Dict]:
    """
    Fetch BTC option instruments from Delta REST API
    Includes retry logic with exponential backoff
    """
    logger.info("🌐 Fetching BTC option instruments (REST)...")

    params = {"contract_types": CONTRACT_TYPES}

    for attempt in range(REST_RETRY_ATTEMPTS):
        try:
            r = requests.get(
                DELTA_REST_PRODUCTS_URL,
                params=params,
                headers=HEADERS,
                timeout=REST_TIMEOUT,
            )
            r.raise_for_status()

            products = r.json().get("result", [])
            options = []

            total = len(products)
            btc_like = 0

            for p in products:
                underlying = str(p.get("underlying_asset", "")).upper()
                symbol = str(p.get("symbol", "")).upper()

                if "BTC" in underlying or symbol.startswith("BTC"):
                    btc_like += 1
                    options.append(
                        {
                            "product_id": p["id"],
                            "symbol": p["symbol"],
                            "strike": float(p.get("strike_price") or 0),
                            "option_type": p.get("contract_type"),
                            "expiry": p.get("settlement_time"),
                        }
                    )

            logger.info(f"📦 Total option products from Delta: {total}")
            logger.info(f"₿ BTC-matching options found: {btc_like}")
            logger.info(f"✅ Loaded {len(options)} BTC options")

            return options

        except requests.RequestException as e:
            if attempt < REST_RETRY_ATTEMPTS - 1:
                wait_time = _exponential_backoff(attempt)
                logger.warning(
                    f"⚠️  API error (attempt {attempt + 1}/{REST_RETRY_ATTEMPTS}): {e}"
                )
                logger.info(f"   Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(
                    f"❌ Failed to fetch options after {REST_RETRY_ATTEMPTS} attempts: {e}"
                )
                return []

        except ValueError as e:
            logger.error(f"❌ Invalid JSON response: {e}")
            return []

    return []


def get_btc_spot_rest() -> Optional[float]:
    """
    Fetch BTC reference price from Delta REST API
    Uses full ticker list and filters safely
    """

    logger.info("🌐 Fetching BTC Spot Price (REST)...")

    try:
        r = requests.get(
            DELTA_REST_TICKERS_URL,
            headers=HEADERS,
            timeout=REST_TIMEOUT
        )

        r.raise_for_status()
        data = r.json()

        tickers = data.get("result", [])

        if not tickers:
            logger.error("❌ No ticker data received")
            return None

        # Preferred search order
        preferred_symbols = ["BTCUSDT", "BTCUSD_PERP", "BTCUSD"]

        for symbol in preferred_symbols:
            for ticker in tickers:
                if ticker.get("symbol") == symbol:
                    price = float(ticker.get("mark_price") or 0)
                    logger.info(f"✅ BTC Price ({symbol}): ${price:,.2f}")
                    return price

        logger.error("❌ BTC symbol not found in ticker list")
        return None

    except Exception as e:
        logger.error(f"❌ Error fetching BTC spot: {e}")
        return None

def get_btc_perp_price() -> Optional[float]:
    """
    Fetch BTC perpetual price from Delta REST API
    """
    try:
        r = requests.get(
            f"{DELTA_REST_TICKERS_URL}/BTCUSD_PERP",
            headers=HEADERS,
            timeout=REST_TIMEOUT,
        )
        r.raise_for_status()
        return float(r.json()["result"]["mark_price"])
    except Exception as e:
        logger.debug(f"Could not fetch BTC perp price: {e}")
        return None
