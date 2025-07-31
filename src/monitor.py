from datetime import datetime
import logging
import time
import os
from dotenv import load_dotenv

from ollama_analyzer import OilPriceChangeAnalyzer
from anomaly_detector import AnomalyDetector
from etl_pipeline import ETLPipeline
from news_aggregator import NewsAggregator
from price_tracker import OilPriceTracker

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('oil_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OilPriceMonitor:
    def __init__(self):
        logger.info("Initializing Oil Price Monitoring System")
        try:
            load_dotenv()
            
            # Initialize components
            self.price_tracker = OilPriceTracker()
            self.anomaly_detector = AnomalyDetector(
                window_size=int(os.getenv('ANOMALY_WINDOW_SIZE', 10)),
                threshold=float(os.getenv('ANOMALY_THRESHOLD', 3.0))
            )
            self.news_aggregator = NewsAggregator()
            self.analyzer = OilPriceChangeAnalyzer(model_name="mistral")
            self.etl = ETLPipeline()
            
            logger.info("All system components initialized successfully")
        except Exception as e:
            logger.error(f"System initialization failed: {e}", exc_info=True)
            raise

    def run(self, interval_minutes=5):
        """Main monitoring loop with enhanced analysis"""
        logger.info(f"Starting monitoring with {interval_minutes} minute intervals")
        
        while True:
            try:
                # Price Monitoring
                logger.info("Fetching latest oil price...")
                price = self.price_tracker.fetch_live_price()
                
                if price is None:
                    logger.warning("Price fetch failed. Using fallback methods...")
                    price = self._get_fallback_price()
                    if price is None:
                        time.sleep(60)
                        continue
                
                logger.info(f"Current Price: ${price:.2f}")
                
                # Anomaly Detection
                is_anomaly, z_score = self.anomaly_detector.detect_anomaly(
                    self.price_tracker.historical_data['price'].tolist()
                )
                
                analysis = None
                if is_anomaly:
                    logger.warning(
                        f"PRICE ANOMALY DETECTED! "
                        f"Price: ${price:.2f}, Z-score: {z_score:.2f}"
                    )
                    
                    # Enhanced News Analysis
                    articles = self.news_aggregator.fetch_price_change_reasons()
                    if articles:
                        logger.info(f"Analyzing {len(articles)} relevant news articles")
                        analysis = self.analyzer.analyze_price_change(articles)
                        
                        if 'reasons' in analysis:
                            logger.info("Price Change Reasons Identified:")
                            for reason in analysis['reasons']:
                                logger.info(f"- {reason}")
                self.etl.store_data({
                    'timestamp': datetime.now(),
                    'price': price,
                    'source': self.price_tracker.last_source  # Now properly defined
                }, is_anomaly, str(analysis) if analysis else None)
                
                
                logger.info(f"Next update in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"Monitoring cycle error: {e}", exc_info=True)
                time.sleep(60)

    def _get_fallback_price(self):
        """Attempt alternative price sources"""
        try:
            # Try getting the most recent valid price
            if not self.price_tracker.historical_data.empty:
                return self.price_tracker.historical_data['price'].iloc[-1]
            return None
        except Exception as e:
            logger.error(f"Fallback price failed: {e}")
            return None

if __name__ == "__main__":
    try:
        logger.info("=== OIL PRICE MONITOR STARTING ===")
        monitor = OilPriceMonitor()
        monitor.run(interval_minutes=5)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.critical(f"Fatal system error: {e}", exc_info=True)
        raise