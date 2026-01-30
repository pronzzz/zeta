import yfinance as yf
from zeta.core.safety.security_manager import SecurityManager
from typing import Optional

class MarketAnalyst:
    def __init__(self, security_manager: SecurityManager):
        self.security = security_manager

    def get_stock_price(self, symbol: str) -> str:
        symbol = symbol.upper().strip()
        
        # Security Check
        if not self.security.verify_action("NETWORK_REQUEST", f"yfinance.Ticker({symbol})", "MEDIUM"):
            return "Action blocked by security."
            
        try:
            stock = yf.Ticker(symbol)
            info = stock.fast_info
            price = info.last_price
            return f"Current price of {symbol}: ${price:.2f}"
        except Exception as e:
            return f"Failed to fetch stock data for {symbol}: {e}"
