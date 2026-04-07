import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance()
        self.exchange.set_sandbox_mode(False)
        
    def get_ohlcv(self, symbol='BTC/USDT', timeframe='1h', limit=200):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv, 
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            logger.info(f"Fetched {len(df)} candles for {symbol} {timeframe}")
            return df
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def get_latest_price(self, symbol='BTC/USDT'):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'price': ticker.get('last'),
                'change': ticker.get('percentage'),
                'high': ticker.get('high'),
                'low': ticker.get('low'),
                'volume': ticker.get('baseVolume', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching ticker: {e}")
            return None


if __name__ == "__main__":
    fetcher = DataFetcher()
    df = fetcher.get_ohlcv('BTC/USDT', '1h', 100)
    print(df.tail())
