"""Cache service for embedding and response caching."""

from app.cache.cache_backend import CacheBackend, InMemoryCache


class CacheService:
    """Service for caching embeddings and search results."""

    def __init__(self, backend: CacheBackend | None = None) -> None:
        self.backend = backend or InMemoryCache()

    async def get_embedding(self, text: str) -> list[float] | None:
        """Get cached embedding for text."""
        key = f"embedding:{text}"
        return await self.backend.get(key)

    async def cache_embedding(
        self, text: str, embedding: list[float], ttl_seconds: int = 86400
    ) -> None:
        """Cache embedding with 24h TTL by default."""
        key = f"embedding:{text}"
        await self.backend.set(key, embedding, ttl_seconds)

    async def get_search_results(self, query: str) -> list[dict] | None:
        """Get cached search results."""
        key = f"search:{query}"
        return await self.backend.get(key)

    async def cache_search_results(
        self, query: str, results: list[dict], ttl_seconds: int = 3600
    ) -> None:
        """Cache search results with 1h TTL by default."""
        key = f"search:{query}"
        await self.backend.set(key, results, ttl_seconds)

    async def clear(self) -> None:
        """Clear all caches."""
        await self.backend.clear()
