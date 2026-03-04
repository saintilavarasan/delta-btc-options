"""Main application window"""

import logging
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtGui import QFont

import data_store
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
)

# Import widgets - use absolute imports
from ui.widgets.option_chain import OptionChainWidget
from ui.widgets.status_bar import StatusBar
from ui.widgets.header import HeaderWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Create main widget
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Add components
        self.header = HeaderWidget()
        layout.addWidget(self.header)

        self.option_chain = OptionChainWidget()
        layout.addWidget(self.option_chain)

        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        logger.info("✅ MainWindow initialized")

    def closeEvent(self, event):
        """Handle window close"""
        logger.info("Closing application...")
        event.accept()
