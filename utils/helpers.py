"""
Helper utilities
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def get_atm_strike(strikes: List[float], spot_price: float) -> Optional[float]:
    """Find at-the-money strike"""
    if not strikes:
        return None
    return min(strikes, key=lambda x: abs(x - spot_price))


def calculate_pcr(options: List[Dict]) -> Optional[float]:
    """Calculate put-call ratio"""
    pe_oi = 0
    ce_oi = 0

    for opt in options:
        if opt.get("type") == "CE":
            ce_oi += opt.get("oi", 0)
        elif opt.get("type") == "PE":
            pe_oi += opt.get("oi", 0)

    if ce_oi == 0:
        return None

    return round(pe_oi / ce_oi, 3)


def group_options_by_strike(options: List[Dict]) -> Dict[float, Dict]:
    """Group options by strike price"""
    grouped = {}
    for opt in options:
        strike = opt.get("strike", 0)
        if strike == 0:
            continue

        if strike not in grouped:
            grouped[strike] = {"CE": {}, "PE": {}}

        opt_type = opt.get("type")
        if opt_type:
            grouped[strike][opt_type] = opt

    return grouped


def get_options_around_atm(options: List[Dict], spot_price: float, levels: int = 6) -> List[Dict]:
    """Get options around ATM strike"""
    strikes = sorted(set(opt.get("strike", 0) for opt in options if opt.get("strike", 0) != 0))

    if not strikes:
        return []

    atm = get_atm_strike(strikes, spot_price)
    try:
        idx = strikes.index(atm)
    except ValueError:
        return options

    start = max(idx - levels, 0)
    end = min(idx + levels + 1, len(strikes))

    target_strikes = strikes[start:end]
    return [opt for opt in options if opt.get("strike") in target_strikes]