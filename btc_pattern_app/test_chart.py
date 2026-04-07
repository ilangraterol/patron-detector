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

print("=== PATRONES DETECTADOS ===")
for p in patterns:
    print(f"- {p.get('name', p.get('type'))}: {p.get('description')}")

print("\n=== GENERANDO GRAFICO ===")
visualizer = ChartVisualizer()
fig = visualizer.create_candlestick_chart(df, patterns)

print(f"Numero de traces en el grafico: {len(fig.data)}")
print("\nLista de traces:")
for i, trace in enumerate(fig.data):
    print(f"  {i}: {trace.name} ({trace.type})")

print("\n=== GRAFICO GENERADO EXITOSAMENTE ===")
print("Puedes ver el grafico en: http://localhost:5000")
