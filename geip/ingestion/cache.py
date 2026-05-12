import json
import os
from datetime import datetime, timedelta
from typing import Any, Callable, TypeVar

import redis

from geip.monitoring import db_logger

T = TypeVar("T")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
DEFAULT_TTL = 300


class CacheService:
    def __init__(self):
        self._client: redis.Redis | None = None
        self._connected = False

    @property
    def client(self) -> redis.Redis | None:
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    decode_responses=True,
                    socket_connect_timeout=2,
                )
                self._client.ping()
                self._connected = True
                db_logger.info("Connected to Redis")
            except redis.ConnectionError as e:
                db_logger.warning(f"Redis connection failed: {e}")
                self._client = None
                self._connected = False
        return self._client

    @property
    def is_connected(self) -> bool:
        if self._client is None:
            return False
        try:
            self._client.ping()
            return True
        except:
            self._connected = False
            return False

    def get(self, key: str) -> Any | None:
        if not self.client:
            db_logger.debug(f"Cache miss (no connection): {key}")
            return None
        try:
            data = self.client.get(key)
            if data:
                db_logger.debug(f"Cache hit: {key}")
                return json.loads(data)
            db_logger.debug(f"Cache miss: {key}")
        except (redis.RedisError, json.JSONDecodeError) as e:
            db_logger.error(f"Cache error on get: {e}")
        return None

    def set(self, key: str, value: Any, ttl: int = DEFAULT_TTL) -> bool:
        if not self.client:
            db_logger.debug(f"Cache set skipped (no connection): {key}")
            return False
        try:
            self.client.setex(key, ttl, json.dumps(value, default=str))
            db_logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except redis.RedisError as e:
            db_logger.error(f"Cache error on set: {e}")
            return False

    def delete(self, key: str) -> bool:
        if not self.client:
            return False
        try:
            self.client.delete(key)
            db_logger.debug(f"Cache deleted: {key}")
            return True
        except redis.RedisError as e:
            db_logger.error(f"Cache error on delete: {e}")
            return False


cache = CacheService()


def cached(key_prefix: str, ttl: int = DEFAULT_TTL):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            cache_key = f"{key_prefix}:{':'.join(str(a) for a in args)}"
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
