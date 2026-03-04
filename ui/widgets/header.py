"""Header widget showing spot price and PCR"""

import logging
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QColor

import data_store

logger = logging.getLogger(__name__)


class HeaderWidget(QWidget):
    """Header showing spot price and key metrics"""

    def __init__(self):
        super().__init__()
        self.init_ui()

        # Subscribe to data changes
        data_store.subscribe_spot_changes(self.on_spot_changed)

        # Setup refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_display)
        self.timer.start(1000)

    def init_ui(self):
        """Initialize UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.spot_label = QLabel("BTC Spot: --")
        self.spot_label.setFont(QFont("Courier", 14, QFont.Bold))
        self.spot_label.setStyleSheet("color: #00ff00;")
        layout.addWidget(self.spot_label)

        self.pcr_label = QLabel("PCR: --")
        self.pcr_label.setFont(QFont("Courier", 12, QFont.Bold))
        self.pcr_label.setStyleSheet("color: #ffaa00;")
        layout.addWidget(self.pcr_label)

        self.connection_label = QLabel("🔴 Disconnected")
        self.connection_label.setFont(QFont("Courier", 10))
        self.connection_label.setStyleSheet("color: #ff5555;")
        layout.addWidget(self.connection_label)

        layout.addStretch()

        self.setLayout(layout)

    def refresh_display(self):
        """Refresh display"""
        spot_price = data_store.get_spot_price()
        if spot_price:
            self.spot_label.setText(f"BTC Spot: ${spot_price:,.2f}")
            self.connection_label.setText("✅ Connected")
            self.connection_label.setStyleSheet("color: #00ff00;")
        else:
            self.connection_label.setText("🔴 Disconnected")
            self.connection_label.setStyleSheet("color: #ff5555;")

    def on_spot_changed(self):
        """Called when spot price changes"""
        self.refresh_display()
