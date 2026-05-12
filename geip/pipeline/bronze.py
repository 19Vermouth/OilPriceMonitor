from datetime import datetime, timezone
from typing import Any

from geip.storage import lake_manager


def ingest_prices(prices: list[dict[str, Any]]):
    lake_manager.write_bronze("prices", prices)


def ingest_news(articles: list[dict[str, Any]]):
    lake_manager.write_bronze("news", articles)


def ingest_risk(risk_data: dict[str, Any]):
    lake_manager.write_bronze("risk", [risk_data])


def ingest_energy(energy_data: list[dict[str, Any]]):
    lake_manager.write_bronze("energy", energy_data)
