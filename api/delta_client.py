"""
Delta Exchange API client
"""

import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class DeltaClient:
    """Client for Delta Exchange REST API"""

    def __init__(self, base_url: str = "https://api.delta.exchange"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def get_products(self, contract_types: str = "call_options,put_options") -> List[Dict]:
        """Get products from Delta Exchange"""
        try:
            response = self.session.get(
                f"{self.base_url}/v2/products",
                params={"contract_types": contract_types},
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("result", [])
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []

    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Get ticker for a symbol"""
        try:
            response = self.session.get(
                f"{self.base_url}/v2/tickers/{symbol}",
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("result")
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return None

    def close(self):
        """Close the session"""
        self.session.close()