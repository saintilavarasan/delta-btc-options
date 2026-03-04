import json
import logging
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import websocket

logger = logging.getLogger(__name__)


class WebSocketWorker(QObject):
    tick_received = pyqtSignal(dict)
    connected = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, symbols):
        super().__init__()
        self.symbols = symbols
        self.ws = None
        self._running = True

    def start_socket(self):
        try:
            logger.info("🌐 Connecting to wss://socket.delta.exchange")

            self.ws = websocket.WebSocketApp(
                "wss://socket.delta.exchange",
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )

            self.ws.run_forever()

        except Exception as e:
            logger.error(f"WebSocket exception: {e}")
            self.error.emit(str(e))

    def stop(self):
        self._running = False
        if self.ws:
            self.ws.close()

    def on_open(self, ws):
        logger.info("✅ WebSocket connected to Delta Exchange")
        self.connected.emit()

        subscribe_payload = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {
                        "name": "v2/ticker",
                        "symbols": self.symbols
                    }
                ]
            }
        }

        ws.send(json.dumps(subscribe_payload))
        logger.info(f"📡 Subscribed to {len(self.symbols)} symbols")

    def on_message(self, ws, message):
        try:
            data = json.loads(message)

            if "symbol" in data:
                self.tick_received.emit(data)

        except Exception as e:
            logger.error(f"Message parse error: {e}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")
        self.error.emit(str(error))

    def on_close(self, ws, close_status_code, close_msg):
        logger.warning("⚠ WebSocket closed")


class DeltaWS:
    def __init__(self, symbols, tick_callback):
        self.thread = QThread()
        self.worker = WebSocketWorker(symbols)

        self.worker.moveToThread(self.thread)

        # Signals
        self.worker.tick_received.connect(tick_callback)
        self.thread.started.connect(self.worker.start_socket)

        self.thread.start()

    def stop(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
