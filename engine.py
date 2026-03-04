"""
Option Chain Engine with performance optimizations
Includes ATM calculation, chain building, and PCR calculation
"""

import logging
from typing import Dict, Optional, List, Tuple

logger = logging.getLogger(__name__)


class OptionEngine:
    """
    Option chain engine with O(1) symbol lookups and performance optimizations
    """

    def __init__(self, options: List[Dict], spot_price: float):
        self.options = options
        self.spot = spot_price
        self.chain: Dict[float, Dict[str, Dict]] = {}
        self.symbol_index: Dict[str, Tuple[float, str]] = {}

        self._build_chain()

    def _build_chain(self):
        """Build option chain structure with symbol indexing"""
        for opt in self.options:
            strike = opt.get("strike", 0)
            if not strike or strike == 0:
                continue

            if strike not in self.chain:
                self.chain[strike] = {"CE": {}, "PE": {}}

            symbol = opt.get("symbol", "")
            option_type = opt.get("option_type", "").lower()

            is_call = "call" in option_type
            is_put = "put" in option_type

            if is_call:
                self.chain[strike]["CE"] = {
                    "symbol": symbol,
                    "ltp": None,
                    "oi": None,
                    "iv": None,
                }
                self.symbol_index[symbol] = (strike, "CE")
            elif is_put:
                self.chain[strike]["PE"] = {
                    "symbol": symbol,
                    "ltp": None,
                    "oi": None,
                    "iv": None,
                }
                self.symbol_index[symbol] = (strike, "PE")

        logger.info(f"✅ Built option chain with {len(self.chain)} strikes")
        logger.info(f"   Symbol index: {len(self.symbol_index)} entries")

    def update_tick(
        self,
        symbol: str,
        ltp: Optional[float] = None,
        oi: Optional[float] = None,
        iv: Optional[float] = None,
    ):
        """Update option data from WebSocket tick with O(1) lookup"""
        if symbol not in self.symbol_index:
            return

        strike, side = self.symbol_index[symbol]
        opt = self.chain[strike][side]

        if ltp is not None:
            opt["ltp"] = ltp
        if oi is not None:
            opt["oi"] = oi
        if iv is not None:
            opt["iv"] = iv

    def _atm_strike(self) -> Optional[float]:
        """Find at-the-money strike"""
        if not self.chain:
            return None
        return min(self.chain.keys(), key=lambda x: abs(x - self.spot))

    @staticmethod
    def _fmt(v: any, width: int = 7) -> str:
        """Format value for display"""
        if v is None:
            return "-".ljust(width)
        if isinstance(v, float):
            return f"{v:.2f}".ljust(width)
        if isinstance(v, int):
            return f"{v}".ljust(width)
        return str(v).ljust(width)

    def print_chain(self, levels: int = 6):
        """Print option chain with ATM centered display"""
        if not self.chain:
            logger.warning("❌ Option chain empty")
            return

        atm = self._atm_strike()
        if not atm:
            logger.warning("❌ Could not find ATM strike")
            return

        strikes = sorted(self.chain.keys())
        try:
            idx = strikes.index(atm)
        except ValueError:
            logger.warning("❌ ATM strike not found in chain")
            return

        start = max(idx - levels, 0)
        end = min(idx + levels + 1, len(strikes))
        view = strikes[start:end]

        print("\n" + "=" * 90)
        print(f"BTC OPTION CHAIN | Spot: ${self.spot:,.2f} | ATM Strike: {atm}")
        print("=" * 90)
        print(
            "CE_LTP   | CE_OI    | CE_IV    || STRIKE   || PE_IV    | PE_OI    | PE_LTP"
        )
        print("-" * 90)

        for strike in view:
            ce = self.chain[strike].get("CE", {})
            pe = self.chain[strike].get("PE", {})

            is_atm = "👈 ATM" if strike == atm else ""

            print(
                f"{self._fmt(ce.get('ltp'), 8)} | "
                f"{self._fmt(ce.get('oi'), 8)} | "
                f"{self._fmt(ce.get('iv'), 8)} || "
                f"{self._fmt(strike, 8)} || "
                f"{self._fmt(pe.get('iv'), 8)} | "
                f"{self._fmt(pe.get('oi'), 8)} | "
                f"{self._fmt(pe.get('ltp'), 8)} {is_atm}"
            )

        print("=" * 90)

    def pcr(self) -> Optional[float]:
        """Calculate put-call ratio"""
        pe_oi = 0
        ce_oi = 0

        for data in self.chain.values():
            ce_oi += data["CE"].get("oi") or 0
            pe_oi += data["PE"].get("oi") or 0

        if ce_oi == 0:
            return None

        return round(pe_oi / ce_oi, 3)

    def get_chain_data(self) -> Dict:
        """Get complete chain data"""
        return dict(self.chain)

    def get_atm_data(self) -> Optional[Dict]:
        """Get ATM strike data"""
        atm = self._atm_strike()
        if not atm:
            return None
        return self.chain.get(atm)

    def get_strikes(self) -> List[float]:
        """Get all available strikes"""
        return sorted(self.chain.keys())

    def update_spot_price(self, price: float):
        """Update spot price"""
        self.spot = price