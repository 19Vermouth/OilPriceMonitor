import os
import time
from functools import wraps
from typing import Any, Callable, TypeVar

import httpx
from pydantic import BaseModel

T = TypeVar("T")


class ConnectorConfig(BaseModel):
    base_url: str
    api_key: str | None = None
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0


class BaseConnector:
    def __init__(self, config: ConnectorConfig):
        self.config = config
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            headers = {"Authorization": f"Bearer {self.config.api_key}"} if self.config.api_key else {}
            self._client = httpx.Client(
                base_url=self.config.base_url,
                timeout=self.config.timeout,
                headers=headers,
            )
        return self._client

    def _retry(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(self: BaseConnector, *args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None
            for attempt in range(self.config.max_retries):
                try:
                    return func(self, *args, **kwargs)
                except (httpx.HTTPError, httpx.TimeoutException) as e:
                    last_exception = e
                    if attempt < self.config.max_retries - 1:
                        delay = self.config.retry_delay * (2**attempt)
                        time.sleep(delay)
            raise last_exception or RuntimeError("Request failed after retries")
        return wrapper

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
