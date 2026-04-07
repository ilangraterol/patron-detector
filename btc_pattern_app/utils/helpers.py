import pandas as pd
import numpy as np
from datetime import datetime


def prepare_data_for_json(df):
    result = {
        'timestamps': df.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        'open': df['open'].tolist(),
        'high': df['high'].tolist(),
        'low': df['low'].tolist(),
        'close': df['close'].tolist(),
        'volume': df['volume'].tolist()
    }
    return result


def format_price(price):
    return f"${price:,.2f}"


def calculate_price_change(df):
    if len(df) < 2:
        return 0, 0
    
    first_price = df['close'].iloc[0]
    last_price = df['close'].iloc[-1]
    
    change = last_price - first_price
    change_percent = (change / first_price) * 100
    
    return change, change_percent


def get_timeframe_limits():
    return {
        '1m': {'limit': 60, 'label': '1 Minuto'},
        '5m': {'limit': 100, 'label': '5 Minutos'},
        '15m': {'limit': 100, 'label': '15 Minutos'},
        '30m': {'limit': 100, 'label': '30 Minutos'},
        '1h': {'limit': 200, 'label': '1 Hora'},
        '4h': {'limit': 200, 'label': '4 Horas'},
        '1d': {'limit': 365, 'label': '1 Día'}
    }


def validate_timeframe(timeframe):
    valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
    return timeframe if timeframe in valid_timeframes else '1h'
