"""
Centralized configuration for Delta BTC Option Chain Terminal
"""

# -------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------
DELTA_API_BASE = "https://api.delta.exchange"
DELTA_REST_PRODUCTS_URL = f"{DELTA_API_BASE}/v2/products"
DELTA_REST_TICKERS_URL = f"{DELTA_API_BASE}/v2/tickers"
DELTA_WS_URL = "wss://socket.delta.exchange"

# -------------------------------------------------
# TRADING PAIRS
# -------------------------------------------------
UNDERLYING = "BTC"
SPOT_SYMBOL = "BTC_USDT"

# -------------------------------------------------
# REST CLIENT SETTINGS
# -------------------------------------------------
REST_TIMEOUT = 10  # seconds
REST_RETRY_ATTEMPTS = 3
REST_RETRY_BACKOFF = 2  # exponential backoff multiplier
REST_RETRY_MAX_WAIT = 30  # seconds

# -------------------------------------------------
# WEBSOCKET SETTINGS
# -------------------------------------------------
WS_RECONNECT_ATTEMPTS = 5
WS_RECONNECT_BACKOFF = 2  # exponential backoff multiplier
WS_RECONNECT_MAX_WAIT = 60  # seconds
WS_PING_INTERVAL = 30  # seconds

# -------------------------------------------------
# UI SETTINGS
# -------------------------------------------------
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
WINDOW_TITLE = "BTC Option Chain - Delta Exchange"

OPTION_CHAIN_LEVELS = 6  # Number of strikes around ATM to display
OPTION_REFRESH_MS = 500  # UI refresh rate in milliseconds

# -------------------------------------------------
# DATA SETTINGS
# -------------------------------------------------
CONTRACT_TYPES = "call_options,put_options"

# -------------------------------------------------
# LOGGING
# -------------------------------------------------
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = "delta_option_chain.log"

# -------------------------------------------------
# THEME COLORS
# -------------------------------------------------
DARK_BG = "#1e1e1e"
DARK_FG = "#ffffff"
DARK_SECONDARY = "#2d2d2d"
DARK_BORDER = "#404040"
ACCENT_PRIMARY = "#0d47a1"
ACCENT_HOVER = "#1565c0"
ACCENT_SUCCESS = "#00ff00"
ACCENT_WARNING = "#ffaa00"
ACCENT_ERROR = "#ff5555"

# -------------------------------------------------
# DARK THEME STYLESHEET
# -------------------------------------------------
DARK_THEME = f"""
    QMainWindow {{
        background-color: {DARK_BG};
        color: {DARK_FG};
    }}
    QWidget {{
        background-color: {DARK_BG};
        color: {DARK_FG};
    }}
    QLabel {{
        color: {DARK_FG};
    }}
    QTreeView {{
        background-color: {DARK_SECONDARY};
        color: {DARK_FG};
        gridline-color: {DARK_BORDER};
        border: 1px solid {DARK_BORDER};
    }}
    QTreeView::item:selected {{
        background-color: {ACCENT_PRIMARY};
    }}
    QComboBox {{
        background-color: {DARK_SECONDARY};
        color: {DARK_FG};
        border: 1px solid {DARK_BORDER};
        padding: 5px;
        border-radius: 3px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {DARK_SECONDARY};
        color: {DARK_FG};
        selection-background-color: {ACCENT_PRIMARY};
    }}
    QPushButton {{
        background-color: {ACCENT_PRIMARY};
        color: {DARK_FG};
        border: none;
        padding: 8px 16px;
        border-radius: 3px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QPushButton:pressed {{
        background-color: #0a3d91;
    }}
    QHeaderView::section {{
        background-color: {ACCENT_PRIMARY};
        color: {DARK_FG};
        padding: 5px;
        border: none;
    }}
"""