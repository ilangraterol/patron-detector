import logging

logger = logging.getLogger(__name__)


class PatternPredictor:
    def __init__(self):
        self.direction_icons = {
            'bullish': '📈',
            'bearish': '📉',
            'neutral': '➡️'
        }
        
    def analyze_patterns(self, patterns, current_price):
        if not patterns:
            return {
                'summary': 'Sin patrones detectados',
                'recommendation': 'Esperar formación de patrones',
                'direction': 'neutral',
                'confidence': 'N/A'
            }
        
        bullish_count = sum(1 for p in patterns if p.get('direction') == 'bullish')
        bearish_count = sum(1 for p in patterns if p.get('direction') == 'bearish')
        
        dominant_direction = 'neutral'
        if bullish_count > bearish_count:
            dominant_direction = 'bullish'
        elif bearish_count > bullish_count:
            dominant_direction = 'bearish'
        
        total_patterns = len(patterns)
        
        analysis = {
            'patterns_found': total_patterns,
            'bullish_patterns': bullish_count,
            'bearish_patterns': bearish_count,
            'direction': dominant_direction,
            'direction_icon': self.direction_icons.get(dominant_direction, '➡️'),
            'patterns_detail': []
        }
        
        for pattern in patterns:
            pattern_info = {
                'type': pattern.get('type', 'unknown'),
                'description': pattern.get('description', ''),
                'direction': pattern.get('direction', 'neutral'),
                'confidence': pattern.get('confidence', 'low'),
                'direction_icon': self.direction_icons.get(pattern.get('direction'), '➡️')
            }
            analysis['patterns_detail'].append(pattern_info)
        
        if dominant_direction == 'bullish':
            analysis['recommendation'] = f'Posición potenciales: LARGE (_LONG) - {bullish_count} patrones alcistas detectados'
            analysis['projection'] = 'SUBIDA'
        elif dominant_direction == 'bearish':
            analysis['recommendation'] = f'Posición potenciales: SHORT - {bearish_count} patrones bajistas detectados'
            analysis['projection'] = 'BAJADA'
        else:
            analysis['recommendation'] = 'Sin dirección clara - esperar más confirmación'
            analysis['projection'] = 'INCERTO'
        
        logger.info(f"Analysis: {analysis['recommendation']}")
        
        return analysis


if __name__ == "__main__":
    predictor = PatternPredictor()
    
    test_patterns = [
        {'type': 'double_bottom', 'direction': 'bullish', 'confidence': 'high', 'description': 'Doble suelo'},
        {'type': 'triangle_ascending', 'direction': 'bullish', 'confidence': 'medium', 'description': 'Triángulo ascendente'}
    ]
    
    result = predictor.analyze_patterns(test_patterns, 50000)
    print(result)
