# Delta BTC Option Chain Terminal

A real-time BTC option chain viewer for Delta Exchange with PyQt5 GUI, WebSocket real-time updates, and advanced features.

## Features

✅ **Real-time Option Chain Display**
- Live LTP, OI, and IV updates via WebSocket
- ATM-centered view with customizable strike levels
- Put-Call Ratio (PCR) calculation

✅ **Robust Architecture**
- Thread-safe data store with synchronization locks
- Automatic WebSocket reconnection with exponential backoff
- REST API error handling with retries
- Structured logging throughout

✅ **User Interface**
- Modern dark theme PyQt5 GUI
- Expiry date filtering
- Live connection status
- Responsive real-time updates

✅ **Performance**
- O(1) symbol lookups using indexing
- Optimized event-driven UI updates
- Efficient option chain processing

## Installation

```bash
# Clone repository
git clone https://github.com/saintilavarasanFile/delta-btc-options.git
cd delta-btc-options

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Project Structure

```
delta-btc-options/
├── config.py                    # Centralized configuration
├── data_store.py                # Thread-safe data store
├── rest_client.py               # REST API client
├── ws_client.py                 # WebSocket client
├── engine.py                    # Option chain logic
├── gui.py                       # GUI entry point
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── FIXES.md                     # Detailed fix documentation
└── ui/
    ├── __init__.py
    ├── theme.py                 # Theme definitions
    ├── main_window.py           # Main window
    └── widgets/
        ├── __init__.py
        ├── header.py            # Header widget
        ├── option_chain.py      # Option chain widget
        └── status_bar.py        # Status bar widget
```

## Configuration

Edit `config.py` to customize:

```python
# API Endpoints
DELTA_API_BASE = "https://api.delta.exchange"

# WebSocket Settings
WS_RECONNECT_ATTEMPTS = 5
WS_RECONNECT_BACKOFF = 2

# UI Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
OPTION_REFRESH_MS = 500
```

## Architecture

### Data Flow

```
REST API (Initial Load)
    ↓
[data_store.py] ← Thread-safe shared state
    ↑             (with callbacks)
WebSocket (Real-time Updates)

    ↓
[gui.py] - PyQt5 UI Components
    ↓
User sees live option chain
```

### Thread Safety

- All global data protected by `threading.Lock()`
- Thread-safe getters/setters in `data_store.py`
- Callbacks for reactive UI updates
- No race conditions

### Error Handling

- REST: Exponential backoff retries (3 attempts)
- WebSocket: Auto-reconnection (5 attempts, 60s max wait)
- Graceful degradation on failures
- Comprehensive error logging

## Usage

1. **Start Application**
   ```bash
   python main.py
   ```

2. **View Option Chain**
   - Application automatically loads BTC options
   - Live updates via WebSocket
   - ATM strike highlighted in blue

3. **Filter by Expiry**
   - Select expiry from dropdown
   - Chain updates automatically
   - "All Expiries" shows complete chain

4. **Monitor Status**
   - Green indicator = Connected
   - Red indicator = Disconnected
   - Auto-reconnects on connection loss

## Performance

- **Spot Price Lookup**: O(1)
- **Symbol Lookup**: O(1) via indexing
- **Option Chain Updates**: O(1) per tick
- **UI Refresh**: 500ms throttled
- **Memory**: ~5-10MB for 500+ options

## Logging

Logs are output to console and `delta_option_chain.log`:

```
2024-02-06 10:15:30 - __main__ - INFO - 🚀 Starting Delta BTC Option Chain Terminal
2024-02-06 10:15:30 - rest_client - INFO - 🌐 Fetching BTC option instruments (REST)...
2024-02-06 10:15:31 - rest_client - INFO - ✅ Loaded 240 BTC options
2024-02-06 10:15:32 - ws_client - INFO - ✅ WebSocket connected to Delta Exchange
```

## Troubleshooting

### WebSocket Connection Issues
- Check internet connection
- Verify Delta Exchange API status
- Logs will show auto-reconnection attempts

### GUI Not Showing
- Ensure PyQt5 is installed: `pip install PyQt5==5.15.9`
- Check X11 forwarding if on remote system

### No Options Loaded
- Verify REST API is accessible
- Check if BTC options exist on Delta Exchange
- Review logs for API errors

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests if applicable
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for educational purposes. Trading derivatives involves risk. Always do your own research and manage risk appropriately.

## Support

For issues and questions:
- Check FIXES.md for known fixes
- Review logs in delta_option_chain.log
- Open GitHub issue with detailed description

## Changelog

### v1.0.0 (Current)
- ✅ Complete refactor with thread safety
- ✅ WebSocket reconnection logic
- ✅ REST error handling
- ✅ PyQt5 UI implementation
- ✅ Performance optimizations
- ✅ Comprehensive logging