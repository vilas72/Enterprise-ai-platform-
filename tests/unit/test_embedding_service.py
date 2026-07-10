"""Unit tests for embedding service."""

import pytest
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.embedding_factory import EmbeddingFactory


@pytest.fixture
def embedding_service():
    """Create embedding service."""
    factory = EmbeddingFactory()
    return EmbeddingService(embedding_factory=factory)


def test_embedding_generation(embedding_service):
    """Test generating embeddings."""
    
    embedding = embedding_service.generate(
        text="Hello world",
        provider="openai",
        model="text-embedding-3-small",
    )

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(x, float) for x in embedding)


def test_embedding_caching(embedding_service):
    """Test embedding caching."""
    
    text = "Test text for caching"
    
    # First call
    emb1 = embedding_service.generate(
        text=text,
        provider="openai",
        model="text-embedding-3-small",
    )
    
    # Second call should use cache (if implemented)
    emb2 = embedding_service.generate(
        text=text,
        provider="openai",
        model="text-embedding-3-small",
    )
    
    # Should be identical
    assert emb1 == emb2


def test_different_texts_different_embeddings(embedding_service):
    """Test different texts produce different embeddings."""
    
    emb1 = embedding_service.generate(
        text="Hello world",
        provider="openai",
        model="text-embedding-3-small",
    )
    
    emb2 = embedding_service.generate(
        text="Goodbye world",
        provider="openai",
        model="text-embedding-3-small",
    )
    
    # Embeddings should be different
    assert emb1 != emb2
