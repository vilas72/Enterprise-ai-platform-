"""Unit tests for hybrid search."""

import pytest
from app.search.hybrid_search import HybridSearch
from app.search.keyword_search import KeywordSearch
from app.vectorstore.vector_service import VectorService
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.embedding_factory import EmbeddingFactory
from app.vectorstore.in_memory_vector_store import InMemoryVectorStore


@pytest.fixture
def hybrid_search():
    """Create hybrid search instance."""
    vector_store = InMemoryVectorStore()
    embedding_factory = EmbeddingFactory()
    embedding_service = EmbeddingService(embedding_factory=embedding_factory)
    vector_service = VectorService(
        embedding_service=embedding_service, vector_store=vector_store
    )

    keyword_search = KeywordSearch()
    keyword_search.index(
        [
            {
                "id": "1",
                "text": "Python is a high-level programming language for beginners",
            },
            {
                "id": "2",
                "text": "JavaScript runs in web browsers and Node.js environments",
            },
            {
                "id": "3",
                "text": "Java is used for enterprise application development",
            },
        ]
    )

    return HybridSearch(
        vector_service=vector_service, keyword_search=keyword_search
    )


@pytest.mark.asyncio
async def test_hybrid_search_returns_results(hybrid_search):
    """Test hybrid search returns results."""
    results = await hybrid_search.search(
        query="Python programming",
        provider="openai",
        model="text-embedding-3-small",
        top_k=3,
    )

    assert len(results) > 0
    assert all(hasattr(r, "document_id") for r in results)


@pytest.mark.asyncio
async def test_hybrid_search_ordering(hybrid_search):
    """Test results are ordered by relevance score."""
    results = await hybrid_search.search(
        query="Python language",
        provider="openai",
        model="text-embedding-3-small",
        top_k=5,
    )

    # Verify scores are in descending order
    if len(results) > 1:
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score


@pytest.mark.asyncio
async def test_hybrid_search_top_k(hybrid_search):
    """Test top_k parameter limits results."""
    results = await hybrid_search.search(
        query="programming",
        provider="openai",
        model="text-embedding-3-small",
        top_k=2,
    )

    assert len(results) <= 2
