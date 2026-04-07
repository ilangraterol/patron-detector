import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

from data.data_fetcher import DataFetcher
from patterns.detector import PatternDetector
from visualization.chart import ChartVisualizer

fetcher = DataFetcher()
df = fetcher.get_ohlcv('BTC/USDT', '1h', 200)

detector = PatternDetector()
patterns = detector.detect_all(df)

visualizer = ChartVisualizer()
fig = visualizer.create_candlestick_chart(df, patterns)
html = visualizer.generate_html(fig)

print(html[:3000])
