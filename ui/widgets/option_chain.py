"""Option chain display widget"""

import logging
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QComboBox,
    QPushButton,
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QColor

import data_store
from config import OPTION_REFRESH_MS

logger = logging.getLogger(__name__)


class OptionChainWidget(QWidget):
    """Main option chain display widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

        # Subscribe to data changes
        data_store.subscribe_option_changes(self.on_data_changed)
        data_store.subscribe_spot_changes(self.on_spot_changed)
        data_store.subscribe_expiry_changes(self.on_expiry_changed)

        # Setup refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_display)
        self.timer.start(OPTION_REFRESH_MS)

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()

        # Expiry selection layout
        expiry_layout = QHBoxLayout()
        expiry_layout.addWidget(QLabel("Select Expiry:"))

        self.expiry_combo = QComboBox()
        self.expiry_combo.currentTextChanged.connect(self.on_expiry_selected)
        expiry_layout.addWidget(self.expiry_combo)

        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.clicked.connect(self.refresh_display)
        expiry_layout.addWidget(self.refresh_button)

        expiry_layout.addStretch()
        layout.addLayout(expiry_layout)

        # Option chain table
        self.tree = QTreeWidget()
        self.tree.setColumnCount(7)
        self.tree.setHeaderLabels(
            ["CE LTP", "CE OI", "CE IV", "STRIKE", "PE IV", "PE OI", "PE LTP"]
        )
        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(1, 100)
        self.tree.setColumnWidth(2, 100)
        self.tree.setColumnWidth(3, 120)
        self.tree.setColumnWidth(4, 100)
        self.tree.setColumnWidth(5, 100)
        self.tree.setColumnWidth(6, 100)
        self.tree.setFont(QFont("Courier", 10))

        layout.addWidget(self.tree)
        self.setLayout(layout)

    def refresh_display(self):
        """Refresh the option chain display"""
        selected_expiry = data_store.get_selected_expiry()

        if selected_expiry:
            options = data_store.get_options_by_expiry(selected_expiry)
        else:
            options = data_store.get_all_options()

        if not options:
            return

        spot_price = data_store.get_spot_price()
        if not spot_price:
            return

        # Group by strike
        strikes_dict = {}
        for opt in options:
            strike = opt.get("strike", 0)
            if strike == 0:
                continue
            if strike not in strikes_dict:
                strikes_dict[strike] = {"CE": {}, "PE": {}}
            strikes_dict[strike][opt.get("type")] = opt

        strikes = sorted(strikes_dict.keys())
        if not strikes:
            return

        # Find ATM
        atm_strike = min(strikes, key=lambda x: abs(x - spot_price))

        # Update tree
        self.tree.clear()
        for strike in strikes:
            ce = strikes_dict[strike].get("CE", {})
            pe = strikes_dict[strike].get("PE", {})

            item = QTreeWidgetItem()
            item.setText(0, f"{ce.get('ltp', '-')}")
            item.setText(1, f"{ce.get('oi', '-')}")
            item.setText(2, f"{ce.get('iv', '-')}")
            item.setText(3, f"{strike}")
            item.setText(4, f"{pe.get('iv', '-')}")
            item.setText(5, f"{pe.get('oi', '-')}")
            item.setText(6, f"{pe.get('ltp', '-')}")

            # Highlight ATM
            if strike == atm_strike:
                for col in range(7):
                    item.setBackground(col, QColor("#0d47a1"))
                    item.setForeground(col, QColor("#ffffff"))

            self.tree.addTopLevelItem(item)

    def update_expiry_combo(self):
        """Update expiry dropdown"""
        current = self.expiry_combo.currentText()
        self.expiry_combo.blockSignals(True)

        expiries = data_store.get_unique_expiries()
        self.expiry_combo.clear()
        self.expiry_combo.addItem("All Expiries")
        self.expiry_combo.addItems(expiries)

        # Restore previous selection
        if current and current != "All Expiries":
            index = self.expiry_combo.findText(current)
            if index >= 0:
                self.expiry_combo.setCurrentIndex(index)

        self.expiry_combo.blockSignals(False)

    def on_data_changed(self):
        """Called when option data changes"""
        self.update_expiry_combo()
        self.refresh_display()

    def on_spot_changed(self):
        """Called when spot price changes"""
        self.refresh_display()

    def on_expiry_changed(self):
        """Called when expiry selection changes"""
        self.refresh_display()

    def on_expiry_selected(self, text: str):
        """Handle expiry selection"""
        if text == "All Expiries":
            data_store.set_selected_expiry(None)
        else:
            data_store.set_selected_expiry(text)
