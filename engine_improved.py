def __init__(self, options, spot_price):
    self.options = options
    self.spot = spot_price
    self.chain = {}
    self.symbol_index = {}  # symbol -> (strike, side) for O(1) lookup
    self._build_chain()

def update_tick(self, symbol, ltp=None, oi=None, iv=None):
    if symbol not in self.symbol_index:
        return
    
    strike, side = self.symbol_index[symbol]
    opt = self.chain[strike][side]
    if ltp is not None:
        opt["ltp"] = ltp
    if oi is not None:
        opt["oi"] = oi
    if iv is not None:
        opt["iv"] = iv