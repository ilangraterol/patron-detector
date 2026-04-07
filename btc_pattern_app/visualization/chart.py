import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
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


class ChartVisualizer:
    def __init__(self):
        self.colors = {
            'bullish': '#26a69a',
            'bearish': '#ef5350',
            'neutral': '#90a4ae'
        }
    
    def create_candlestick_chart(self, df, patterns=None):
        fig = go.Figure()
        
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='BTC/USDT',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ))
        
        if patterns:
            self._add_pattern_overlays(fig, df, patterns)
        
        fig.update_layout(
            title=dict(
                text='BTC/USDT - Gráfico en Tiempo Real',
                font=dict(size=20)
            ),
            xaxis_title='Tiempo',
            yaxis_title='Precio (USDT)',
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=600,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def _add_pattern_overlays(self, fig, df, patterns):
        for pattern in patterns:
            pattern_type = pattern.get('type', '')
            
            if 'triangle' in pattern_type:
                self._add_triangle_lines(fig, df, pattern)
            elif 'double_top' in pattern_type:
                self._add_double_top_lines(fig, df, pattern)
            elif 'double_bottom' in pattern_type:
                self._add_double_bottom_lines(fig, df, pattern)
            elif 'head_shoulders' in pattern_type:
                self._add_head_shoulders_lines(fig, df, pattern)
            elif 'triple' in pattern_type:
                self._add_triple_lines(fig, df, pattern)
            elif 'flag' in pattern_type:
                self._add_flag_lines(fig, df, pattern)
            elif 'pennant' in pattern_type:
                self._add_pennant_lines(fig, df, pattern)
    
    def _add_triangle_lines(self, fig, df, pattern):
        high = df['high'].values
        low = df['low'].values
        highs_idx = find_peaks(high, 3)
        lows_idx = find_valleys(low, 3)
        
        if len(highs_idx) >= 2 and len(lows_idx) >= 2:
            recent_highs_idx = highs_idx[-4:]
            recent_lows_idx = lows_idx[-4:]
            
            for i, idx in enumerate(recent_highs_idx[:-1]):
                fig.add_trace(go.Scatter(
                    x=[df.index[idx], df.index[recent_highs_idx[i+1]]],
                    y=[df['high'].values[idx], df['high'].values[recent_highs_idx[i+1]]],
                    mode='lines',
                    line=dict(color='yellow', width=2, dash='dash'),
                    name=f'Resistencia {pattern["type"]}',
                    showlegend=False
                ))
            
            for i, idx in enumerate(recent_lows_idx[:-1]):
                fig.add_trace(go.Scatter(
                    x=[df.index[idx], df.index[recent_lows_idx[i+1]]],
                    y=[df['low'].values[idx], df['low'].values[recent_lows_idx[i+1]]],
                    mode='lines',
                    line=dict(color='cyan', width=2, dash='dash'),
                    name=f'Soporte {pattern["type"]}',
                    showlegend=False
                ))
    
    def _add_double_top_lines(self, fig, df, pattern):
        recent_candles = df.tail(50)
        max_price = recent_candles['high'].max()
        
        fig.add_hline(
            y=max_price,
            line_dash="dash",
            line_color="red",
            annotation_text="Doble Techo",
            annotation_position="top right"
        )
    
    def _add_double_bottom_lines(self, fig, df, pattern):
        recent_candles = df.tail(50)
        min_price = recent_candles['low'].min()
        
        fig.add_hline(
            y=min_price,
            line_dash="dash",
            line_color="green",
            annotation_text="Doble Suelo",
            annotation_position="bottom right"
        )
    
    def _add_head_shoulders_lines(self, fig, df, pattern):
        recent_candles = df.tail(30)
        max_price = recent_candles['high'].max()
        
        fig.add_hline(
            y=max_price,
            line_dash="dot",
            line_color="orange",
            annotation_text="HCH",
            annotation_position="top right"
        )
    
    def _add_triple_lines(self, fig, df, pattern):
        pattern_type = pattern.get('type', '')
        
        if 'top' in pattern_type:
            recent_candles = df.tail(50)
            max_price = recent_candles['high'].max()
            
            fig.add_hline(
                y=max_price,
                line_dash="dash",
                line_color="red",
                annotation_text="Triple Techo",
                annotation_position="top right"
            )
        else:
            recent_candles = df.tail(50)
            min_price = recent_candles['low'].min()
            
            fig.add_hline(
                y=min_price,
                line_dash="dash",
                line_color="green",
                annotation_text="Triple Suelo",
                annotation_position="bottom right"
            )
    
    def _add_flag_lines(self, fig, df, pattern):
        recent = df.tail(20)
        
        fig.add_trace(go.Scatter(
            x=[recent.index[0], recent.index[5]],
            y=[recent['close'].values[0], recent['close'].values[5]],
            mode='lines',
            line=dict(color='yellow', width=1),
            name='Bandera',
            showlegend=False
        ))
    
    def _add_pennant_lines(self, fig, df, pattern):
        recent = df.tail(15)
        
        fig.add_trace(go.Scatter(
            x=[recent.index[0], recent.index[-1]],
            y=[recent['high'].max(), recent['low'].min()],
            mode='lines',
            line=dict(color='cyan', width=1),
            name='Banderín',
            showlegend=False
        ))
    
    def generate_html(self, fig):
        return fig.to_html(full_html=False, include_plotlyjs='cdn')


if __name__ == "__main__":
    from data.data_fetcher import DataFetcher
    from patterns.detector import PatternDetector
    
    fetcher = DataFetcher()
    df = fetcher.get_ohlcv('BTC/USDT', '1h', 200)
    
    detector = PatternDetector()
    patterns = detector.detect_all(df)
    
    visualizer = ChartVisualizer()
    fig = visualizer.create_candlestick_chart(df, patterns)
    
    html = visualizer.generate_html(fig)
    print("Chart generated successfully")
