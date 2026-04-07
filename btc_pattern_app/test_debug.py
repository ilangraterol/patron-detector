import re
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

match = re.search(r'<div id="([^"]+)"', html)
if match:
    print('Div ID found:', match.group(1))
else:
    print('No div ID found')

print('---HTML START---')
print(html[:1000])
print('---HTML END---')
