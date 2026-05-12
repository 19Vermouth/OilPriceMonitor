import logging
import sys
from typing import Optional

LOG_LEVEL = "INFO"


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    log_level = level or LOG_LEVEL
    
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger


prices_logger = setup_logger("geip.prices")
news_logger = setup_logger("geip.news")
alerts_logger = setup_logger("geip.alerts")
pipeline_logger = setup_logger("geip.pipeline")
api_logger = setup_logger("geip.api")
db_logger = setup_logger("geip.database")
