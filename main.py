"""
Main entry point for Delta BTC Option Chain Terminal
Stable version – No auto close issue
"""

import sys
import logging
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox

import data_store
from rest_client import load_options_from_rest, get_btc_spot_rest
from ws_client import DeltaWS
from ui.main_window import MainWindow
from config import LOG_LEVEL, LOG_FORMAT, DARK_THEME


# ------------------ Logging Setup ------------------

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
)

logger = logging.getLogger(__name__)


# ------------------ Option Initialization ------------------

def initialize_option_data(options):
    logger.info("Initializing option data...")
    data_store.clear_option_data()

    for opt in options:
        strike = opt.get("strike")
        if not strike:
            continue

        expiry_raw = opt.get("expiry")

        try:
            if isinstance(expiry_raw, (int, float)):
                expiry_dt = datetime.fromtimestamp(expiry_raw)
            else:
                expiry_dt = datetime.fromisoformat(
                    expiry_raw.replace("Z", "+00:00")
                )

            expiry = expiry_dt.strftime("%d-%b-%Y")
        except Exception:
            continue

        option_type = opt.get("option_type", "").lower()

        data_store.set_option_data(
            opt["symbol"],
            {
                "symbol": opt["symbol"],
                "strike": strike,
                "type": "CE" if "call" in option_type else "PE",
                "expiry": expiry,
                "ltp": None,
                "oi": None,
                "iv": None,
            },
        )

    logger.info(f"✅ Initialized {len(data_store.get_all_options())} options")


# ------------------ WebSocket Tick Handler ------------------

def on_ws_tick(data):
    symbol = data.get("symbol")
    if not symbol:
        return

    option = data_store.get_option_data(symbol)
    if not option:
        return

    updates = {}

    if "mark_price" in data:
        updates["ltp"] = data["mark_price"]

    if "oi" in data:
        updates["oi"] = data["oi"]

    if "iv" in data:
        updates["iv"] = data["iv"]

    if updates:
        data_store.update_option_data(symbol, updates)


# ------------------ Main Application ------------------

def main():
    logger.info("🚀 Starting Delta BTC Option Chain Terminal")

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    # Create and show main window
    window = MainWindow()
    window.show()

    try:
        # Step 1: Load Options
        logger.info("Loading options from REST...")
        options = load_options_from_rest()

        if not options:
            QMessageBox.warning(window, "Warning", "No options loaded from REST.")
        else:
            initialize_option_data(options)

            # Step 2: Load Spot Price
            logger.info("Fetching BTC spot...")
            spot_price = get_btc_spot_rest()

            if spot_price:
                data_store.set_spot_price(spot_price)
            else:
                QMessageBox.warning(window, "Warning", "Failed to fetch BTC spot price.")

            # Step 3: Start WebSocket (IMPORTANT: store reference in window)
            try:
                window.ws_client = DeltaWS(
                    [opt["symbol"] for opt in options],
                    on_ws_tick
                )
                logger.info("WebSocket started successfully")

            except Exception as e:
                logger.error(f"WebSocket startup error: {e}")
                QMessageBox.warning(window, "WebSocket Error", str(e))

    except Exception as e:
        logger.critical(f"Startup error: {e}", exc_info=True)
        QMessageBox.critical(window, "Startup Error", str(e))

    # Start Qt event loop
    exit_code = app.exec_()

    logger.info(f"Application exited with code {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
