from utils.logger import setup_logging

class OilPriceMonitor:
    def __init__(self):
        self.logger = setup_logging()
        
    def run(self):
        try:
            self.logger.info("Starting oil price monitoring")
            # Main logic here
        except Exception as e:
            self.logger.error(f"Monitoring failed: {str(e)}", exc_info=True)
            raise
        