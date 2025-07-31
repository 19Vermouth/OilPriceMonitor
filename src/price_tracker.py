import yfinance as yf
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class OilPriceTracker:
    def __init__(self):
        self.historical_data = pd.DataFrame(columns=['timestamp', 'price', 'source'])
        self.last_source = "Not fetched yet"  # Initialize last_source
        self.symbols = {
            'WTI': 'CL=F',
            'Brent': 'BZ=F'
        }
        
    def fetch_live_price(self):
        """Try multiple data sources to get oil prices"""
        price, source = self._fetch_yfinance()
        
        if price is not None:
            self.last_source = source  # Update last_source when successful
            self._store_price(price, source)
            return price
            
        # Fallback to cached data if available
        if not self.historical_data.empty:
            logger.warning("Using last cached price as fallback")
            self.last_source = "Cache"  # Track cache usage
            return self.historical_data['price'].iloc[-1]
            
        self.last_source = "Failed"  # Track complete failure
        return None
    
    def _fetch_yfinance(self):
        """Fetch prices using yfinance"""
        try:
            for name, symbol in self.symbols.items():
                ticker = yf.Ticker(symbol)
                data = ticker.history(period='1d', interval='1m')
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    return last_price, f"yfinance-{name}"
                    
        except Exception as e:
            logger.error(f"yfinance error: {e}")
            
        return None, None
    
    def _store_price(self, price, source):
        """Store price with timestamp and source"""
        self.historical_data.loc[len(self.historical_data)] = {
            'timestamp': datetime.now(),
            'price': price,
            'source': source
        }