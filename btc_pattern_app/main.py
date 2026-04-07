import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

from flask import Flask, render_template, jsonify, request
import logging

from data.data_fetcher import DataFetcher
from patterns.detector import PatternDetector
from visualization.chart import ChartVisualizer
from analysis.predictor import PatternPredictor
from utils.helpers import prepare_data_for_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')

data_fetcher = DataFetcher()
pattern_detector = PatternDetector()
chart_visualizer = ChartVisualizer()
pattern_predictor = PatternPredictor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    try:
        timeframe = request.args.get('timeframe', '1h')
        
        logger.info(f"Fetching data for timeframe: {timeframe}")
        
        df = data_fetcher.get_ohlcv('BTC/USDT', timeframe, 200)
        
        if df.empty:
            return jsonify({'error': 'No se pudieron obtener datos'})
        
        ticker = data_fetcher.get_latest_price('BTC/USDT')
        
        patterns = pattern_detector.detect_all(df)
        
        analysis = pattern_predictor.analyze_patterns(patterns, df['close'].iloc[-1])
        
        fig = chart_visualizer.create_candlestick_chart(df, patterns)
        chart_html = chart_visualizer.generate_html(fig)
        
        chart_data = {
            'data': prepare_data_for_json(df),
            'shapes': [],
            'annotations': []
        }
        
        return jsonify({
            'chart': chart_data,
            'ticker': ticker,
            'analysis': analysis,
            'timeframe': timeframe
        })
        
    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        return jsonify({'error': str(e)})


@app.route('/api/ticker')
def get_ticker():
    try:
        ticker = data_fetcher.get_latest_price('BTC/USDT')
        return jsonify(ticker)
    except Exception as e:
        logger.error(f"Error in get_ticker: {e}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    logger.info("Iniciando BTC Pattern Detector...")
    logger.info("Accede a: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
