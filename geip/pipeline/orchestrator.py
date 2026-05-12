import logging
from datetime import datetime, timezone

from geip.pipeline import bronze, silver, gold
from geip.monitoring import pipeline_logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def run_pipeline():
    pipeline_logger.info(f"Starting pipeline at {datetime.now(timezone.utc)}")
    
    try:
        pipeline_logger.info("Running Silver transformations...")
        silver.run_all()
        pipeline_logger.info("Silver transformations complete")
    except Exception as e:
        pipeline_logger.error(f"Silver transformation failed: {e}")
    
    try:
        pipeline_logger.info("Running Gold aggregations...")
        gold.run_all()
        pipeline_logger.info("Gold aggregations complete")
    except Exception as e:
        pipeline_logger.error(f"Gold aggregation failed: {e}")
    
    pipeline_logger.info(f"Pipeline complete at {datetime.now(timezone.utc)}")


def run_bronze_ingestion(prices=None, news=None, risk=None, energy=None):
    if prices:
        try:
            bronze.ingest_prices([p.model_dump() if hasattr(p, 'model_dump') else p for p in prices])
            pipeline_logger.info(f"Ingested {len(prices)} prices to Bronze")
        except Exception as e:
            pipeline_logger.error(f"Bronze price ingestion failed: {e}")
    
    if news:
        try:
            bronze.ingest_news(news)
            pipeline_logger.info(f"Ingested {len(news)} news to Bronze")
        except Exception as e:
            pipeline_logger.error(f"Bronze news ingestion failed: {e}")


if __name__ == "__main__":
    run_pipeline()
