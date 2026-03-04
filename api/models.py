"""
Data models for options and ticker data
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TickerData:
    """Ticker data model"""
    symbol: str
    mark_price: Optional[float] = None
    last_price: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    open_interest: Optional[float] = None
    iv: Optional[float] = None
    timestamp: Optional[datetime] = None

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'mark_price': self.mark_price,
            'last_price': self.last_price,
            'bid': self.bid,
            'ask': self.ask,
            'open_interest': self.open_interest,
            'iv': self.iv,
            'timestamp': self.timestamp
        }


@dataclass
class OptionData:
    """Option data model"""
    symbol: str
    strike: float
    option_type: str  # 'CE' or 'PE'
    expiry: str
    ltp: Optional[float] = None
    oi: Optional[float] = None
    iv: Optional[float] = None

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'strike': self.strike,
            'option_type': self.option_type,
            'expiry': self.expiry,
            'ltp': self.ltp,
            'oi': self.oi,
            'iv': self.iv
        }