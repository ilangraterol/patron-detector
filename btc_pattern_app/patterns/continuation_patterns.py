import numpy as np
import logging

logger = logging.getLogger(__name__)


def find_peaks(data, order=3):
    peaks = []
    for i in range(order, len(data) - order):
        is_peak = True
        for j in range(1, order + 1):
            if data[i] <= data[i - j] or data[i] <= data[i + j]:
                is_peak = False
                break
        if is_peak:
            peaks.append(i)
    return np.array(peaks)


def find_valleys(data, order=3):
    valleys = []
    for i in range(order, len(data) - order):
        is_valley = True
        for j in range(1, order + 1):
            if data[i] >= data[i - j] or data[i] >= data[i + j]:
                is_valley = False
                break
        if is_valley:
            valleys.append(i)
    return np.array(valleys)


def format_time_range(df, indices):
    if len(indices) < 2:
        return ""
    start_time = df.index[indices[0]]
    end_time = df.index[indices[-1]]
    return f"{start_time.strftime('%d/%m/%Y %I:%M %p')} - {end_time.strftime('%d/%m/%Y %I:%M %p')}"


class PatternDetector:
    def __init__(self, window=5, order=3):
        self.window = window
        self.order = order
        
    def find_swing_highs(self, df):
        high = df['high'].values
        return find_peaks(high, self.order)
    
    def find_swing_lows(self, df):
        low = df['low'].values
        return find_valleys(low, self.order)
    
    def find_swing_points(self, df):
        highs_idx = self.find_swing_highs(df)
        lows_idx = self.find_swing_lows(df)
        return highs_idx, lows_idx


class ContinuationPatternDetector(PatternDetector):
    def __init__(self, window=5, order=3):
        super().__init__(window, order)
        
    def detect_triangle_ascending(self, df, threshold=0.02):
        highs_idx, lows_idx = self.find_swing_points(df)
        
        if len(highs_idx) < 2 or len(lows_idx) < 2:
            return None
            
        highs = df['high'].values[highs_idx]
        lows = df['low'].values[lows_idx]
        
        if len(highs) < 2 or len(lows) < 2:
            return None
            
        high_slope = (highs[-1] - highs[0]) / len(highs)
        low_slope = (lows[-1] - lows[0]) / len(lows)
        
        if high_slope < 0 and low_slope > 0:
            return {
                'type': 'triangle_ascending',
                'name': 'Ascending Triangle (Triángulo Ascendente)',
                'direction': 'bullish',
                'confidence': 'medium',
                'description': 'Patrón de continuación alcista - resistencia horizontal con soporte ascendente',
                'help': 'El triángulo ascendente tiene resistencia horizontal y soporte ascendente. Generalmente es un patrón alcista que indica que los compradores están ganando fuerza.',
                'time_range': format_time_range(df, list(highs_idx[-4:]) + list(lows_idx[-4:]))
            }
        return None
    
    def detect_triangle_descending(self, df, threshold=0.02):
        highs_idx, lows_idx = self.find_swing_points(df)
        
        if len(highs_idx) < 2 or len(lows_idx) < 2:
            return None
            
        highs = df['high'].values[highs_idx]
        lows = df['low'].values[lows_idx]
        
        if len(highs) < 2 or len(lows) < 2:
            return None
            
        high_slope = (highs[-1] - highs[0]) / len(highs)
        low_slope = (lows[-1] - lows[0]) / len(lows)
        
        if high_slope < 0 and low_slope < 0:
            if abs(high_slope) > abs(low_slope):
                return {
                    'type': 'triangle_descending',
                    'name': 'Descending Triangle (Triángulo Descendente)',
                    'direction': 'bearish',
                    'confidence': 'medium',
                    'description': 'Patrón de continuación bajista - soporte horizontal con resistencia descendente',
                    'help': 'El triángulo descendente tiene soporte horizontal y resistencia descendente. Generalmente es un patrón bajista que indica que los vendedores están ganando fuerza.',
                    'time_range': format_time_range(df, list(highs_idx[-4:]) + list(lows_idx[-4:]))
                }
        return None
    
    def detect_triangle_symmetric(self, df, threshold=0.02):
        highs_idx, lows_idx = self.find_swing_points(df)
        
        if len(highs_idx) < 2 or len(lows_idx) < 2:
            return None
            
        highs = df['high'].values[highs_idx]
        lows = df['low'].values[lows_idx]
        
        if len(highs) < 2 or len(lows) < 2:
            return None
            
        high_slope = (highs[-1] - highs[0]) / len(highs)
        low_slope = (lows[-1] - lows[0]) / len(lows)
        
        if high_slope < 0 and low_slope > 0:
            return {
                'type': 'triangle_symmetric',
                'name': 'Symmetric Triangle (Triángulo Simétrico)',
                'direction': 'neutral',
                'confidence': 'low',
                'description': 'Patrón de consolidación - dirección unsure',
                'help': 'El triángulo simétrico está formado por soporte ascendente y resistencia descendente. Es un patrón de consolidación que puede romper en cualquier dirección.',
                'time_range': format_time_range(df, list(highs_idx[-4:]) + list(lows_idx[-4:]))
            }
        return None
    
    def detect_flag(self, df, threshold=0.03):
        highs_idx, lows_idx = self.find_swing_points(df)
        
        if len(highs_idx) < 3:
            return None
            
        recent_highs = df['high'].values[highs_idx[-3:]]
        recent_lows = df['low'].values[lows_idx[-3:]] if len(lows_idx) >= 3 else None
        
        if len(recent_highs) >= 3 and recent_lows is not None and len(recent_lows) >= 3:
            first_move = recent_highs[1] - recent_highs[0]
            pullback = recent_lows[2] - recent_lows[1]
            
            if first_move > 0 and abs(pullback / first_move) < 0.5:
                return {
                    'type': 'flag',
                    'name': 'Flag (Bandera)',
                    'direction': 'bullish',
                    'confidence': 'medium',
                    'description': 'Patrón de continuación alcista - bandera',
                    'help': 'La bandera es un patrón de continuación que se forma después de un movimiento fuerte (asta). El precio se consolida en un canal estrecho antes de continuar en la misma dirección.',
                    'time_range': format_time_range(df, list(highs_idx[-4:]) + list(lows_idx[-4:]))
                }
            
            first_move_bearish = recent_lows[1] - recent_lows[0]
            pullback_bearish = recent_highs[2] - recent_highs[1]
            
            if first_move_bearish < 0 and abs(pullback_bearish / first_move_bearish) < 0.5:
                return {
                    'type': 'flag',
                    'name': 'Flag (Bandera)',
                    'direction': 'bearish',
                    'confidence': 'medium',
                    'description': 'Patrón de continuación bajista - bandera',
                    'help': 'La bandera bajista es un patrón de continuación que se forma después de un movimiento bajista fuerte. El precio se consolida en un canal estrecho antes de continuar bajando.',
                    'time_range': format_time_range(df, list(highs_idx[-4:]) + list(lows_idx[-4:]))
                }
        return None
    
    def detect_pennant(self, df, threshold=0.02):
        highs_idx, lows_idx = self.find_swing_points(df)
        
        if len(highs_idx) < 4 or len(lows_idx) < 4:
            return None
            
        recent_highs = df['high'].values[highs_idx[-4:]]
        recent_lows = df['low'].values[lows_idx[-4:]]
        
        high_range = np.max(recent_highs) - np.min(recent_highs)
        low_range = np.max(recent_lows) - np.min(recent_lows)
        
        price_range = df['close'].values[-1] - df['close'].values[0]
        
        if high_range < abs(price_range) * 0.3 and low_range < abs(price_range) * 0.3:
            direction = 'bullish' if price_range > 0 else 'bearish'
            return {
                'type': 'pennant',
                'name': 'Pennant (Banderín)',
                'direction': direction,
                'confidence': 'medium',
                'description': f'Patrón de continuación {direction} - banderín',
                'help': 'El banderín es un patrón de continuación similar a la bandera, pero con líneas de soporte y resistencia convergentes. Se forma después de un movimiento fuerte.',
                'time_range': format_time_range(df, list(highs_idx[-4:]) + list(lows_idx[-4:]))
            }
        return None
    
    def detect_all(self, df):
        patterns = []
        
        triangle_asc = self.detect_triangle_ascending(df)
        if triangle_asc:
            patterns.append(triangle_asc)
            
        triangle_desc = self.detect_triangle_descending(df)
        if triangle_desc:
            patterns.append(triangle_desc)
            
        triangle_sym = self.detect_triangle_symmetric(df)
        if triangle_sym:
            patterns.append(triangle_sym)
            
        flag = self.detect_flag(df)
        if flag:
            patterns.append(flag)
            
        pennant = self.detect_pennant(df)
        if pennant:
            patterns.append(pennant)
            
        return patterns


if __name__ == "__main__":
    from data.data_fetcher import DataFetcher
    fetcher = DataFetcher()
    df = fetcher.get_ohlcv('BTC/USDT', '1h', 200)
    detector = ContinuationPatternDetector()
    patterns = detector.detect_all(df)
    print("Patrones detectados:", patterns)
