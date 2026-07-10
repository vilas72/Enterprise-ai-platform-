"""Caching layer for response and embedding caching."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class CacheBackend(ABC, Generic[T]):
    """Abstract cache backend."""

    @abstractmethod
    async def get(self, key: str) -> T | None:
        """Get value from cache."""
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: T, ttl_seconds: int = 3600) -> None:
        """Set value in cache with TTL."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cache."""
        raise NotImplementedError


class InMemoryCache(CacheBackend[T]):
    """In-memory cache implementation."""

    def __init__(self) -> None:
        self._cache: dict[str, tuple[T, float]] = {}
        self._ttl: dict[str, float] = {}

    async def get(self, key: str) -> T | None:
        if key not in self._cache:
            return None
        value, expiry = self._cache[key]
        # TODO: Add TTL checking
        return value

    async def set(self, key: str, value: T, ttl_seconds: int = 3600) -> None:
        import time
        expiry = time.time() + ttl_seconds
        self._cache[key] = (value, expiry)
        self._ttl[key] = expiry

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)
        self._ttl.pop(key, None)

    async def clear(self) -> None:
        self._cache.clear()
        self._ttl.clear()


class RedisCache(CacheBackend[T]):
    """Redis-backed cache implementation (Phase 2)."""

    def __init__(self, redis_url: str = "redis://localhost:6379") -> None:
        self.redis_url = redis_url
        self._client = None  # Lazy loaded

    async def _ensure_connected(self) -> None:
        """Lazy load Redis connection."""
        if self._client is None:
            try:
                import aioredis
                self._client = await aioredis.from_url(self.redis_url)
            except ImportError:
                raise ImportError(
                    "aioredis not installed. Install with: pip install aioredis"
                )

    async def get(self, key: str) -> T | None:
        await self._ensure_connected()
        value = await self._client.get(key)  # type: ignore
        return value

    async def set(self, key: str, value: T, ttl_seconds: int = 3600) -> None:
        await self._ensure_connected()
        await self._client.setex(key, ttl_seconds, value)  # type: ignore

    async def delete(self, key: str) -> None:
        await self._ensure_connected()
        await self._client.delete(key)  # type: ignore

    async def clear(self) -> None:
        await self._ensure_connected()
        await self._client.flushdb()  # type: ignore
