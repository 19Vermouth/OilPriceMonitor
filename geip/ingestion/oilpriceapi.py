import os
from datetime import datetime, timezone
from typing import Any

import httpx

from geip.ingestion.base import BaseConnector, ConnectorConfig
from geip.schemas import CrudeType, PriceData
from geip.monitoring import prices_logger


class OilPriceAPIConnector(BaseConnector):
    BASE_URL = "https://api.oilpriceapi.com/v1"

    def __init__(self):
        super().__init__(ConnectorConfig(
            base_url=self.BASE_URL,
            api_key=os.getenv("OILPRICEAPI_KEY"),
            timeout=30,
            max_retries=3,
        ))
        self.has_api_key = bool(os.getenv("OILPRICEAPI_KEY"))

    def get_latest_prices(self) -> list[PriceData]:
        if not self.has_api_key:
            prices_logger.warning("No API key found, using fallback prices")
            return self._get_fallback_prices()

        try:
            prices_logger.info("Fetching prices from OilPriceAPI...")
            response = self.client.get("/latest_price")
            response.raise_for_status()
            data = response.json()

            prices = []
            for item in data.get("data", []):
                crude_type = self._map_location(item.get("location", ""))
                if crude_type:
                    prices.append(PriceData(
                        crude_type=crude_type,
                        price=float(item.get("price", 0)),
                        timestamp=datetime.now(timezone.utc),
                    ))
            
            prices_logger.info(f"Successfully fetched {len(prices)} prices from API")
            return prices
        except httpx.HTTPStatusError as e:
            prices_logger.error(f"HTTP error fetching prices: {e.response.status_code}")
            return self._get_fallback_prices()
        except httpx.RequestError as e:
            prices_logger.error(f"Request error: {e}")
            return self._get_fallback_prices()
        except Exception as e:
            prices_logger.error(f"Unexpected error: {e}")
            return self._get_fallback_prices()

    def _map_location(self, location: str) -> CrudeType | None:
        mapping = {
            "WTI": CrudeType.WTI,
            "BRENT": CrudeType.BRENT,
            "DUBAI": CrudeType.DUBAI,
            "OPEC": CrudeType.OPEC_BASKET,
        }
        for key, value in mapping.items():
            if key in location.upper():
                return value
        return CrudeType.WTI

    def _get_fallback_prices(self) -> list[PriceData]:
        prices_logger.info("Using fallback prices")
        fallback = {
            CrudeType.WTI: 78.50,
            CrudeType.BRENT: 82.30,
            CrudeType.DUBAI: 80.15,
            CrudeType.OPEC_BASKET: 79.00,
        }
        return [
            PriceData(crude_type=crude, price=price, timestamp=datetime.now(timezone.utc))
            for crude, price in fallback.items()
        ]


connector = OilPriceAPIConnector()


def get_prices() -> list[PriceData]:
    return connector.get_latest_prices()
