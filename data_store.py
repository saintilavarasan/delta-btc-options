"""
Shared thread-safe in-memory data store for Delta BTC Option Chain Terminal

All components (REST, WS, UI) read/write here with proper synchronization.
"""

from threading import Lock
from typing import Dict, Any, Optional, Callable, List

# Thread locks for synchronization
_option_data_lock = Lock()
_spot_data_lock = Lock()
_expiry_lock = Lock()

# -------------------------------------------------
# Live Option Data
# symbol -> {
#   symbol, strike, type, expiry,
#   ltp, oi, iv
# }
# -------------------------------------------------
_option_data: Dict[str, Dict[str, Any]] = {}

# -------------------------------------------------
# Spot Price
# -------------------------------------------------
_spot_data: Dict[str, Optional[float]] = {
    "price": None
}

# -------------------------------------------------
# Currently Selected Expiry (UI controlled)
# Example: "28-Mar-2025"
# -------------------------------------------------
_selected_expiry: Optional[str] = None

# -------------------------------------------------
# Callbacks for data changes
# -------------------------------------------------
_option_data_callbacks: List[Callable] = []
_spot_data_callbacks: List[Callable] = []
_expiry_callbacks: List[Callable] = []


def subscribe_option_changes(callback: Callable) -> None:
    """Subscribe to option data changes"""
    _option_data_callbacks.append(callback)


def subscribe_spot_changes(callback: Callable) -> None:
    """Subscribe to spot price changes"""
    _spot_data_callbacks.append(callback)


def subscribe_expiry_changes(callback: Callable) -> None:
    """Subscribe to expiry selection changes"""
    _expiry_callbacks.append(callback)


def _notify_option_changes() -> None:
    """Notify all subscribers of option data changes"""
    for callback in _option_data_callbacks:
        try:
            callback()
        except Exception as e:
            import logging
            logging.error(f"Error in option data callback: {e}")


def _notify_spot_changes() -> None:
    """Notify all subscribers of spot price changes"""
    for callback in _spot_data_callbacks:
        try:
            callback()
        except Exception as e:
            import logging
            logging.error(f"Error in spot data callback: {e}")


def _notify_expiry_changes() -> None:
    """Notify all subscribers of expiry changes"""
    for callback in _expiry_callbacks:
        try:
            callback()
        except Exception as e:
            import logging
            logging.error(f"Error in expiry callback: {e}")


# -------------------------------------------------
# OPTION DATA OPERATIONS
# -------------------------------------------------

def set_option_data(symbol: str, data: Dict[str, Any]) -> None:
    """Thread-safe set option data"""
    with _option_data_lock:
        _option_data[symbol] = data
    _notify_option_changes()


def update_option_data(symbol: str, updates: Dict[str, Any]) -> None:
    """Thread-safe update specific option fields"""
    with _option_data_lock:
        if symbol in _option_data:
            _option_data[symbol].update(updates)
    _notify_option_changes()


def get_option_data(symbol: Optional[str] = None) -> Dict:
    """Thread-safe get option data"""
    with _option_data_lock:
        if symbol:
            return _option_data.get(symbol, {}).copy()
        return dict(_option_data)


def clear_option_data() -> None:
    """Clear all option data"""
    with _option_data_lock:
        _option_data.clear()
    _notify_option_changes()


def get_all_options() -> list:
    """Get all options as a list"""
    with _option_data_lock:
        return list(_option_data.values())


def get_options_by_expiry(expiry: str) -> list:
    """Get options filtered by expiry"""
    with _option_data_lock:
        return [opt for opt in _option_data.values() if opt.get("expiry") == expiry]


def get_unique_expiries() -> list:
    """Get all unique expiry dates"""
    with _option_data_lock:
        expiries = set()
        for opt in _option_data.values():
            expiry = opt.get("expiry")
            if expiry:
                expiries.add(expiry)
        return sorted(list(expiries))


# -------------------------------------------------
# SPOT PRICE OPERATIONS
# -------------------------------------------------

def set_spot_price(price: float) -> None:
    """Thread-safe set spot price"""
    with _spot_data_lock:
        if _spot_data["price"] != price:
            _spot_data["price"] = price
    _notify_spot_changes()


def get_spot_price() -> Optional[float]:
    """Thread-safe get spot price"""
    with _spot_data_lock:
        return _spot_data["price"]


# -------------------------------------------------
# EXPIRY SELECTION OPERATIONS
# -------------------------------------------------

def set_selected_expiry(expiry: Optional[str]) -> None:
    """Thread-safe set selected expiry"""
    with _expiry_lock:
        global _selected_expiry
        if _selected_expiry != expiry:
            _selected_expiry = expiry
    _notify_expiry_changes()


def get_selected_expiry() -> Optional[str]:
    """Thread-safe get selected expiry"""
    with _expiry_lock:
        return _selected_expiry


# -------------------------------------------------
# BULK OPERATIONS
# -------------------------------------------------

def get_state_snapshot() -> Dict[str, Any]:
    """Get a complete snapshot of current state"""
    with _option_data_lock, _spot_data_lock, _expiry_lock:
        return {
            "options": dict(_option_data),
            "spot_price": _spot_data["price"],
            "selected_expiry": _selected_expiry
        }