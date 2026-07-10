"""Unit tests for cache service."""

import pytest
from app.cache.cache_service import CacheService
from app.cache.cache_backend import InMemoryCache


@pytest.mark.asyncio
async def test_cache_embedding():
    """Test caching embeddings."""
    cache = CacheService(backend=InMemoryCache())

    text = "Hello world"
    embedding = [0.1, 0.2, 0.3]

    await cache.cache_embedding(text, embedding)
    retrieved = await cache.get_embedding(text)

    assert retrieved == embedding


@pytest.mark.asyncio
async def test_cache_miss():
    """Test cache miss returns None."""
    cache = CacheService(backend=InMemoryCache())

    result = await cache.get_embedding("non-existent")
    assert result is None


@pytest.mark.asyncio
async def test_cache_search_results():
    """Test caching search results."""
    cache = CacheService(backend=InMemoryCache())

    query = "What is Python?"
    results = [
        {"id": "1", "text": "Python is a language", "score": 0.95}
    ]

    await cache.cache_search_results(query, results)
    retrieved = await cache.get_search_results(query)

    assert retrieved == results


@pytest.mark.asyncio
async def test_cache_clear():
    """Test clearing cache."""
    cache = CacheService(backend=InMemoryCache())

    await cache.cache_embedding("test", [0.1, 0.2])
    await cache.clear()

    result = await cache.get_embedding("test")
    assert result is None
