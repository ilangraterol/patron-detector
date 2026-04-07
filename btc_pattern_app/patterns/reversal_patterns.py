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


class ReversalPatternDetector:
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
    
    def detect_double_top(self, df, threshold=0.03):
        highs_idx, _ = self.find_swing_points(df)
        
        if len(highs_idx) < 2:
            return None
            
        recent_highs_idx = highs_idx[-4:] if len(highs_idx) >= 4 else highs_idx
        recent_highs = df['high'].values[recent_highs_idx]
        
        if len(recent_highs) < 2:
            return None
            
        max_high = np.max(recent_highs)
        min_high = np.min(recent_highs)
        
        if (max_high - min_high) / max_high < threshold:
            return None
            
        peaks = []
        for idx in recent_highs_idx:
            if abs(df['high'].values[idx] - max_high) / max_high < threshold:
                peaks.append(idx)
                
        if len(peaks) >= 2:
            return {
                'type': 'double_top',
                'name': 'Double Top (Doble Techo)',
                'direction': 'bearish',
                'confidence': 'high',
                'description': 'Patrón de reversión bajista - doble techo',
                'help': 'El doble techo es un patrón de reversión bajista que se forma cuando el precio alcanza dos máximos similares. Indica que la tendencia alcista podría estar agotándose.',
                'time_range': format_time_range(df, peaks)
            }
        return None
    
    def detect_double_bottom(self, df, threshold=0.03):
        _, lows_idx = self.find_swing_points(df)
        
        if len(lows_idx) < 2:
            return None
            
        recent_lows_idx = lows_idx[-4:] if len(lows_idx) >= 4 else lows_idx
        recent_lows = df['low'].values[recent_lows_idx]
        
        if len(recent_lows) < 2:
            return None
            
        max_low = np.max(recent_lows)
        min_low = np.min(recent_lows)
        
        if (max_low - min_low) / max_low < threshold:
            return None
            
        bottoms = []
        for idx in recent_lows_idx:
            if abs(df['low'].values[idx] - min_low) / min_low < threshold:
                bottoms.append(idx)
                
        if len(bottoms) >= 2:
            return {
                'type': 'double_bottom',
                'name': 'Double Bottom (Doble Suelo)',
                'direction': 'bullish',
                'confidence': 'high',
                'description': 'Patrón de reversión alcista - doble suelo',
                'help': 'El doble suelo es un patrón de reversión alcista que se forma cuando el precio alcanza dos mínimos similares. Indica que la tendencia bajista podría estar agotándose.',
                'time_range': format_time_range(df, bottoms)
            }
        return None
    
    def detect_head_shoulders(self, df, threshold=0.05):
        highs_idx, _ = self.find_swing_points(df)
        
        if len(highs_idx) < 3:
            return None
            
        recent_highs_idx = highs_idx[-5:] if len(highs_idx) >= 5 else highs_idx
        recent_highs = df['high'].values[recent_highs_idx]
        
        if len(recent_highs) < 3:
            return None
            
        head_idx = np.argmax(recent_highs)
        
        if head_idx == 0 or head_idx == len(recent_highs) - 1:
            return None
            
        left_shoulder = recent_highs[head_idx - 1] if head_idx > 0 else None
        right_shoulder = recent_highs[head_idx + 1] if head_idx < len(recent_highs) - 1 else None
        
        if left_shoulder is None or right_shoulder is None:
            return None
            
        head_height = recent_highs[head_idx]
        
        if (head_height - left_shoulder) / head_height > threshold and \
           (head_height - right_shoulder) / head_height > threshold:
            if abs(left_shoulder - right_shoulder) / head_height < 0.1:
                return {
                    'type': 'head_shoulders',
                    'name': 'Head and Shoulders (Hombro-Cabeza-Hombro)',
                    'direction': 'bearish',
                    'confidence': 'high',
                    'description': 'Patrón de reversión bajista - Hombro Cabeza Hombro',
                    'help': 'El patrón Hombro-Cabeza-Hombro es un patrón de reversión bajista con tres picos: el del medio (cabeza) es más alto que los otros dos (hombros). Indica el fin de una tendencia.',
                    'time_range': format_time_range(df, recent_highs_idx)
                }
        return None
    
    def detect_inverse_head_shoulders(self, df, threshold=0.05):
        _, lows_idx = self.find_swing_points(df)
        
        if len(lows_idx) < 3:
            return None
            
        recent_lows_idx = lows_idx[-5:] if len(lows_idx) >= 5 else lows_idx
        recent_lows = df['low'].values[recent_lows_idx]
        
        if len(recent_lows) < 3:
            return None
            
        head_idx = np.argmin(recent_lows)
        
        if head_idx == 0 or head_idx == len(recent_lows) - 1:
            return None
            
        left_shoulder = recent_lows[head_idx - 1] if head_idx > 0 else None
        right_shoulder = recent_lows[head_idx + 1] if head_idx < len(recent_lows) - 1 else None
        
        if left_shoulder is None or right_shoulder is None:
            return None
            
        head_depth = recent_lows[head_idx]
        
        if (left_shoulder - head_depth) / left_shoulder > threshold and \
           (right_shoulder - head_depth) / right_shoulder > threshold:
            if abs(left_shoulder - right_shoulder) / left_shoulder < 0.1:
                return {
                    'type': 'inverse_head_shoulders',
                    'name': 'Inverse Head and Shoulders (HCH Invertido)',
                    'direction': 'bullish',
                    'confidence': 'high',
                    'description': 'Patrón de reversión alcista - HCH Invertido',
                    'help': 'El HCH Invertido es un patrón de reversión alcista con tres mínimos: el del medio (cabeza) es más bajo que los otros dos (hombros). Indica el fin de una tendencia bajista.',
                    'time_range': format_time_range(df, recent_lows_idx)
                }
        return None
    
    def detect_triple_top(self, df, threshold=0.03):
        highs_idx, _ = self.find_swing_points(df)
        
        if len(highs_idx) < 3:
            return None
            
        recent_highs_idx = highs_idx[-6:] if len(highs_idx) >= 6 else highs_idx
        recent_highs = df['high'].values[recent_highs_idx]
        
        if len(recent_highs) < 3:
            return None
            
        max_high = np.max(recent_highs)
        
        peaks = []
        for idx in recent_highs_idx:
            if abs(df['high'].values[idx] - max_high) / max_high < threshold:
                peaks.append(idx)
                
        if len(peaks) >= 3:
            return {
                'type': 'triple_top',
                'name': 'Triple Top (Triple Techo)',
                'direction': 'bearish',
                'confidence': 'high',
                'description': 'Patrón de reversión bajista - triple techo',
                'help': 'El triple techo es un patrón de reversión bajista que se forma cuando el precio alcanza tres máximos similares. Es una señal fuerte de que la tendencia alcista podría revertirse.',
                'time_range': format_time_range(df, peaks)
            }
        return None
    
    def detect_triple_bottom(self, df, threshold=0.03):
        _, lows_idx = self.find_swing_points(df)
        
        if len(lows_idx) < 3:
            return None
            
        recent_lows_idx = lows_idx[-6:] if len(lows_idx) >= 6 else lows_idx
        recent_lows = df['low'].values[recent_lows_idx]
        
        if len(recent_lows) < 3:
            return None
            
        min_low = np.min(recent_lows)
        
        bottoms = []
        for idx in recent_lows_idx:
            if abs(df['low'].values[idx] - min_low) / min_low < threshold:
                bottoms.append(idx)
                
        if len(bottoms) >= 3:
            return {
                'type': 'triple_bottom',
                'name': 'Triple Bottom (Triple Suelo)',
                'direction': 'bullish',
                'confidence': 'high',
                'description': 'Patrón de reversión alcista - triple suelo',
                'help': 'El triple suelo es un patrón de reversión alcista que se forma cuando el precio alcanza tres mínimos similares. Es una señal fuerte de que la tendencia bajista podría revertirse.',
                'time_range': format_time_range(df, bottoms)
            }
        return None
    
    def detect_all(self, df):
        patterns = []
        
        double_top = self.detect_double_top(df)
        if double_top:
            patterns.append(double_top)
            
        double_bottom = self.detect_double_bottom(df)
        if double_bottom:
            patterns.append(double_bottom)
            
        hcs = self.detect_head_shoulders(df)
        if hcs:
            patterns.append(hcs)
            
        ihcs = self.detect_inverse_head_shoulders(df)
        if ihcs:
            patterns.append(ihcs)
            
        triple_top = self.detect_triple_top(df)
        if triple_top:
            patterns.append(triple_top)
            
        triple_bottom = self.detect_triple_bottom(df)
        if triple_bottom:
            patterns.append(triple_bottom)
            
        return patterns


if __name__ == "__main__":
    from data.data_fetcher import DataFetcher
    fetcher = DataFetcher()
    df = fetcher.get_ohlcv('BTC/USDT', '1h', 200)
    detector = ReversalPatternDetector()
    patterns = detector.detect_all(df)
    print("Patrones detectados:", patterns)
