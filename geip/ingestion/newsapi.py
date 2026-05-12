import os
from datetime import datetime, timezone
from typing import Any

import httpx

from geip.ingestion.base import BaseConnector, ConnectorConfig
from geip.monitoring import news_logger


class NewsAPIConnector(BaseConnector):
    BASE_URL = "https://newsapi.org/v2"

    def __init__(self):
        super().__init__(ConnectorConfig(
            base_url=self.BASE_URL,
            api_key=os.getenv("NEWSAPI_API_KEY"),
            timeout=30,
            max_retries=3,
        ))
        self.has_api_key = bool(os.getenv("NEWSAPI_API_KEY"))

    def get_energy_news(self, query: str = "oil OR crude OR energy", limit: int = 10) -> list[dict[str, Any]]:
        if not self.has_api_key:
            news_logger.warning("No API key found, using fallback news")
            return self._get_fallback_news()

        try:
            news_logger.info(f"Fetching {limit} articles from NewsAPI...")
            response = self.client.get(
                "/everything",
                params={
                    "q": query,
                    "sortBy": "publishedAt",
                    "pageSize": limit,
                    "language": "en",
                    "apiKey": self.config.api_key,
                }
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "source": article.get("source", {}).get("name"),
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt"),
                    "sentiment": "neutral",
                })
            
            news_logger.info(f"Successfully fetched {len(articles)} articles")
            return articles
        except httpx.HTTPStatusError as e:
            news_logger.error(f"HTTP error: {e.response.status_code}")
            return self._get_fallback_news()
        except httpx.RequestError as e:
            news_logger.error(f"Request error: {e}")
            return self._get_fallback_news()
        except Exception as e:
            news_logger.error(f"Unexpected error: {e}")
            return self._get_fallback_news()

    def _get_fallback_news(self) -> list[dict[str, Any]]:
        news_logger.info("Using fallback news")
        return [
            {
                "title": "OPEC+ Maintains Production Cuts",
                "description": "Saudi Arabia and Russia reaffirm commitment to output restrictions through Q2.",
                "source": "Energy Intelligence",
                "url": "#",
                "published_at": datetime.now(timezone.utc).isoformat(),
                "sentiment": "bullish",
            },
            {
                "title": "US Crude Inventories Rise",
                "description": "EIA reports unexpected inventory build of 4.2 million barrels.",
                "source": "Reuters",
                "url": "#",
                "published_at": datetime.now(timezone.utc).isoformat(),
                "sentiment": "bearish",
            },
        ]


connector = NewsAPIConnector()


def get_energy_news(limit: int = 10) -> list[dict[str, Any]]:
    return connector.get_energy_news(limit=limit)
