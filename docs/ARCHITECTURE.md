# Architecture Guide

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   PyQt5 User Interface                       │
│              (ui/main_window.py, ui/widgets.py)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ (Data Subscription)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Thread-Safe Data Store (data_store.py)            │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ Option Data  │ Spot Data    │ Expiry Selection       │ │
│  │ (with Locks) │ (with Locks) │ (with Locks)           │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└────────┬────────────────────────────────────┬───────────────┘
         │                                    │
    (Write Updates)                    (Write Updates)
         │                                    │
         ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│  REST Client         │          │  WebSocket Client    │
│  (rest_client.py)    │          │  (ws_client.py)      │
│                      │          │                      │
│ • Retry Logic        │          │ • Auto-Reconnect     │
│ • Error Handling     │          │ • Error Handling     │
│ • Exponential Backoff│          │ • Exponential Backoff│
└──────────────────────┘          └──────────────────────┘
         │                                    │
         │ (HTTP Requests)          (WebSocket Stream)
         │                                    │
         ▼                                    ▼
┌────────────────────────────────────────────────────────────┐
│            Delta Exchange API                              │
│  • REST: https://api.delta.exchange/v2/products           │
│  • WS:   wss://socket.delta.exchange                       │
└────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface (ui/)

**main_window.py**
- Main application window
- Manages window properties and layout
- Initializes all components

**widgets.py**
- OptionChainWidget: Displays real-time option chain
- StatusBar: Shows connection status and metrics

**theme.py**
- Dark theme stylesheet
- Color and font definitions

**styles.py**
- Additional styling utilities
- Color and font constants

### 2. Data Store (data_store.py)

**Thread-Safe Operations**
```python
# All operations use locks
_option_data_lock = Lock()
_spot_data_lock = Lock()
_expiry_lock = Lock()

# Safe getters/setters
def set_option_data(symbol, data):
    with _option_data_lock:
        _option_data[symbol] = data
        _notify_option_changes()  # Trigger UI updates
```

**Event System**
- subscribe_option_changes()
- subscribe_spot_changes()
- subscribe_expiry_changes()

### 3. REST Client (rest_client.py)

**Error Handling Strategy**
```
Request
  ├─ Success → Return data
  └─ Failure → Retry Logic
      ├─ Attempt 1: Wait 2^0 = 1s
      ├─ Attempt 2: Wait 2^1 = 2s
      ├─ Attempt 3: Wait 2^2 = 4s
      └─ Max wait: 30s
```

**Graceful Degradation**
- Returns empty list on fatal error
- Application continues operation
- User is notified via logs

### 4. WebSocket Client (ws_client.py)

**Reconnection Strategy**
```
Connection
  ├─ Success → Connected
  └─ Failure → Reconnection Attempt
      ├─ Attempt 1: Wait 2^0 = 1s
      ├─ Attempt 2: Wait 2^1 = 2s
      ├─ Attempt 3: Wait 2^2 = 4s
      ├─ Attempt 4: Wait 2^3 = 8s
      ├─ Attempt 5: Wait 2^4 = 16s
      └─ Max: 60s per attempt
```

**Event Handlers**
- on_open(): Subscribe to tickers
- on_message(): Process ticker updates
- on_error(): Log errors
- on_close(): Attempt reconnection

### 5. Option Engine (engine.py)

**Data Structure**
```python
chain = {
    50000: {  # Strike
        "CE": {  # Call Option
            "symbol": "BTC-30DEC21-50000-CE",
            "ltp": 1000,
            "oi": 100,
            "iv": 0.5
        },
        "PE": {  # Put Option
            "symbol": "BTC-30DEC21-50000-PE",
            "ltp": 800,
            "oi": 90,
            "iv": 0.45
        }
    }
}

symbol_index = {
    "BTC-30DEC21-50000-CE": (50000, "CE"),
    "BTC-30DEC21-50000-PE": (50000, "PE"),
}
```

**Performance Optimization**
- Symbol lookup: O(1) via index
- Chain update: O(1) direct access
- ATM calculation: O(n log n) sorted strikes

### 6. API Models (api/models.py)

**Data Models**
- TickerData: Market data
- OptionData: Option information

### 7. Utilities (utils/)

**helpers.py**
- get_atm_strike(): Find at-the-money
- calculate_pcr(): Put-call ratio
- group_options_by_strike(): Group data
- get_options_around_atm(): Range query

**formatting.py**
- format_price(): Currency formatting
- format_oi(): Open interest display
- format_iv(): Implied volatility display

## Data Flow

### Initialization Flow
```
main.py
  ├─ setup_logging()
  ├─ load_options_from_rest()
  │   └─ REST Client (retry logic)
  │       └─ Delta Exchange API
  ├─ get_btc_spot_rest()
  │   └─ REST Client (retry logic)
  │       └─ Delta Exchange API
  ├─ initialize_option_data()
  │   └─ data_store.set_option_data()
  │       └─ Notify subscribers
  ├─ DeltaWS()
  │   └─ WebSocket connection
  │       └─ auto_start=True
  ├─ QApplication()
  │   └─ MainWindow()
  │       └─ UI initialization
  │           └─ Subscribe to data changes
  └─ app.exec_()
```

### Real-Time Update Flow
```
WebSocket Message Received
  ├─ json.loads() → Parse
  ├─ on_tick() → Process
  │   ├─ data_store.get_option_data() → Get existing
  │   ├─ Prepare updates dict
  │   └─ data_store.update_option_data()
  │       └─ Acquire _option_data_lock
  │           ├─ Update fields
  │           └─ _notify_option_changes()
  │               └─ Call all subscribers
  │                   └─ OptionChainWidget.on_data_changed()
  │                       └─ UI.refresh_display()
  │                           └─ Update tree widget
  └─ Display updated in UI
```

## Threading Model

### Main Thread
- PyQt5 event loop
- UI rendering
- User interactions

### WebSocket Thread
- Daemon thread
- WebSocket.run_forever()
- Calls on_message() in same thread

### Lock Protection
```
REST Thread (Main)       WebSocket Thread       UI Thread (Main)
      │                          │                    │
      │─── set_spot_price() ────►│                    │
      │    (acquire lock)        │                    │
      │                          │                    │
      │                          │─── update_option() ├─ set_option_data()
      │                          │    (acquire lock)  │  (acquire lock)
      │◄─ Notify callbacks ◄──────────────────────────┤  Refresh UI
      │                                                │
```

## Configuration System

**config.py** organizes settings into sections:
- API_ENDPOINTS: URL configuration
- TRADING_PAIRS: Market symbols
- REST_CLIENT_SETTINGS: Retry and timeout
- WEBSOCKET_SETTINGS: Reconnection strategy
- UI_SETTINGS: Window and refresh rates
- LOGGING: Log levels and files
- FEATURES: Feature flags
- PERFORMANCE: Optimization parameters

## Error Handling Strategy

### REST API Errors
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except RequestException:
    # Retry with exponential backoff
    # Max retries: 3
    # Max wait: 30 seconds
    # On final failure: Return empty list
```

### WebSocket Errors
```python
def on_error(self, ws, error):
    logger.error(f"WebSocket error: {error}")
    # on_close will be called automatically

def on_close(self, ws, close_status_code, close_msg):
    logger.warning(f"WebSocket closed: {close_msg}")
    # Attempt reconnection with exponential backoff
    # Max retries: 5
    # Max wait: 60 seconds
```

### Data Store Errors
```python
def _notify_option_changes():
    for callback in _option_data_callbacks:
        try:
            callback()
        except Exception as e:
            # Log but don't crash
            logging.error(f"Callback error: {e}")
```

## Performance Considerations

### Memory Usage
- MAX_OPTIONS_IN_MEMORY: 10,000
- Each
