"""
Additional styling utilities
"""

from PyQt5.QtGui import QFont, QColor


class Colors:
    """Color constants"""
    PRIMARY = "#0d47a1"
    PRIMARY_HOVER = "#1565c0"
    PRIMARY_PRESSED = "#0a3d91"
    
    BACKGROUND = "#1e1e1e"
    SURFACE = "#2d2d2d"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    
    SUCCESS = "#00ff00"
    WARNING = "#ffaa00"
    ERROR = "#ff5252"
    
    ATM_HIGHLIGHT = "#0d47a1"
    CALL_COLOR = "#00ff00"
    PUT_COLOR = "#ff5252"


class Fonts:
    """Font constants"""
    @staticmethod
    def monospace(size: int = 10, bold: bool = False) -> QFont:
        font = QFont("Courier", size)
        font.setBold(bold)
        return font
    
    @staticmethod
    def header(size: int = 12) -> QFont:
        return QFont("Courier", size, QFont.Bold)