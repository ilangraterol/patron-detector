from data.data_fetcher import DataFetcher
from patterns.detector import PatternDetector
from visualization.chart import ChartVisualizer

fetcher = DataFetcher()
df = fetcher.get_ohlcv('BTC/USDT', '1h', 200)

detector = PatternDetector()
patterns = detector.detect_all(df)

visualizer = ChartVisualizer()
fig = visualizer.create_candlestick_chart(df, patterns)
chart_json = visualizer.generate_figure_json(fig)

print('Type:', type(chart_json))
if isinstance(chart_json, dict):
    print('Keys:', chart_json.keys())
    if 'data' in chart_json:
        print('Data type:', type(chart_json['data']))
        print('Data length:', len(chart_json['data']))
        if len(chart_json['data']) > 0:
            print('First trace type:', chart_json['data'][0].get('type', 'unknown'))
            print('First trace name:', chart_json['data'][0].get('name', 'no name'))