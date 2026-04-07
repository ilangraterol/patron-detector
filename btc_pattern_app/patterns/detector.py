from patterns.continuation_patterns import ContinuationPatternDetector
from patterns.reversal_patterns import ReversalPatternDetector
import logging

logger = logging.getLogger(__name__)


class PatternDetector:
    def __init__(self, window=5, order=3):
        self.continuation_detector = ContinuationPatternDetector(window, order)
        self.reversal_detector = ReversalPatternDetector(window, order)
        
    def detect_all(self, df):
        all_patterns = []
        
        continuation_patterns = self.continuation_detector.detect_all(df)
        all_patterns.extend(continuation_patterns)
        
        reversal_patterns = self.reversal_detector.detect_all(df)
        all_patterns.extend(reversal_patterns)
        
        logger.info(f"Total patterns detected: {len(all_patterns)}")
        
        return all_patterns


if __name__ == "__main__":
    from data.data_fetcher import DataFetcher
    fetcher = DataFetcher()
    df = fetcher.get_ohlcv('BTC/USDT', '1h', 200)
    detector = PatternDetector()
    patterns = detector.detect_all(df)
    print("Patrones detectados:", patterns)
