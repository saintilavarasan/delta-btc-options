"""Status bar widget"""

import logging
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

import data_store

logger = logging.getLogger(__name__)


class StatusBar(QWidget):
    """Status bar showing connection and system info"""

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

    def init_ui(self):
        """Initialize UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        self.status_label = QLabel("🔄 Loading...")
        self.status_label.setStyleSheet("color: #ffaa00;")
        self.status_label.setFont(QFont("Courier", 9))
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.info_label = QLabel("Ready")
        self.info_label.setStyleSheet("color: #00ff00;")
        self.info_label.setFont(QFont("Courier", 9))
        layout.addWidget(self.info_label)

        self.setLayout(layout)

    def refresh(self):
        """Update status display"""
        options_count = len(data_store.get_all_options())
        spot = data_store.get_spot_price()

        if options_count > 0 and spot:
            self.status_label.setText("✅ Live")
            self.status_label.setStyleSheet("color: #00ff00;")
        else:
            self.status_label.setText("🔄 Loading...")
            self.status_label.setStyleSheet("color: #ffaa00;")

        self.info_label.setText(f"Options: {options_count}")
