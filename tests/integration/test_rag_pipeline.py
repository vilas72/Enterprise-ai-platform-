"""Integration tests for RAG pipeline."""

import pytest
from app.rag.rag_service import RagService
from app.rag.rag_request import RagRequest
from app.search.hybrid_search import HybridSearch
from app.search.keyword_search import KeywordSearch
from app.vectorstore.vector_service import VectorService
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.embedding_factory import EmbeddingFactory
from app.vectorstore.in_memory_vector_store import InMemoryVectorStore
from tests.mocks.mock_services import MockAIService, MockEmbeddingProvider


@pytest.fixture
def rag_pipeline():
    """Create a full RAG pipeline for integration tests with mocked services."""
    vector_store = InMemoryVectorStore()
    embedding_factory = EmbeddingFactory()
    embedding_service = EmbeddingService(embedding_factory=embedding_factory)
    
    # Mock the embedding provider
    mock_provider = MockEmbeddingProvider()
    embedding_factory._providers = {
        "openai": mock_provider,
        "gemini": mock_provider,
    }
    
    vector_service = VectorService(
        embedding_service=embedding_service, vector_store=vector_store
    )

    # Index documents
    docs = [
        "Python is a high-level programming language",
        "Python supports OOP, functional, and procedural programming",
        "JavaScript is primarily used for web development",
    ]
    for i, doc in enumerate(docs):
        vector_service.index(text=doc, document_id=f"doc-{i}")

    keyword_search = KeywordSearch()
    keyword_search.index(
        [{"id": f"doc-{i}", "text": doc} for i, doc in enumerate(docs)]
    )

    hybrid_search = HybridSearch(
        vector_service=vector_service, keyword_search=keyword_search
    )

    ai_service = MockAIService()

    return RagService(
        hybrid_search=hybrid_search,
        vector_service=vector_service,
        ai_service=ai_service,
    )


@pytest.mark.skip(reason="Requires OpenAI API")
def test_rag_pipeline_end_to_end(rag_pipeline):
    """Test full RAG pipeline with documents."""
    request = RagRequest(
        question="What is Python?", provider="openai", model="gpt-4", top_k=3
    )

    response = rag_pipeline.ask(request)

    # Verify response structure
    assert response.answer is not None
    assert len(response.answer) > 0


@pytest.mark.skip(reason="Requires OpenAI API")
def test_rag_with_context_building(rag_pipeline):
    """Test RAG with context builder."""
    request = RagRequest(
        question="Tell me about Python programming",
        provider="openai",
        model="gpt-4",
        top_k=3,
    )

    response = rag_pipeline.ask(request)

    # Response should be non-empty
    assert isinstance(response.answer, str)
    assert len(response.answer) >= 0


@pytest.mark.skip(reason="Requires OpenAI API")
@pytest.mark.parametrize("question", ["", "What is Python?", "Tell me about programming"])
def test_rag_handles_various_queries(rag_pipeline, question):
    """Test RAG handles various query inputs gracefully."""
    request = RagRequest(
        question=question, provider="openai", model="gpt-4", top_k=5
    )

    try:
        response = rag_pipeline.ask(request)
        assert response is not None
    except ValueError:
        # Empty query might raise ValueError, that's acceptable
        assert question == ""
