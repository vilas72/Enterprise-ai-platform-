"""Tests for reranking integration in hybrid search."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.reranking.reranker import Reranker
from app.reranking.rerank_request import RerankRequest
from app.reranking.rerank_result import RerankResult
from app.rag.retrieved_document import RetrievedDocument
from app.search.hybrid_search import HybridSearch
from app.search.keyword_search import KeywordSearch
from app.search.rank_fusion import RankFusion
from app.search.search_result import SearchResult
from app.search.reranking_service import RerangingService
from app.vectorstore.vector_service import VectorService
from app.vectorstore.vector_search_result import VectorSearchResult
from app.vectorstore.vector_document import VectorDocument


@pytest.fixture
def mock_vector_service():
    """Create mock vector service."""
    service = MagicMock(spec=VectorService)
    return service


@pytest.fixture
def mock_keyword_search():
    """Create mock keyword search."""
    search = MagicMock(spec=KeywordSearch)
    return search


@pytest.fixture
def mock_reranker():
    """Create mock reranker."""
    reranker = AsyncMock(spec=Reranker)
    return reranker


@pytest.fixture
def sample_vector_results():
    """Create sample vector search results."""
    documents = [
        VectorDocument(
            id="doc1",
            text="Python programming guide",
            embedding=[0.1] * 768,
            metadata={"source": "docs"},
        ),
        VectorDocument(
            id="doc2",
            text="Python best practices",
            embedding=[0.2] * 768,
            metadata={"source": "blog"},
        ),
        VectorDocument(
            id="doc3",
            text="Python performance tips",
            embedding=[0.3] * 768,
            metadata={"source": "article"},
        ),
    ]
    return [
        VectorSearchResult(document=documents[0], score=0.95),
        VectorSearchResult(document=documents[1], score=0.87),
        VectorSearchResult(document=documents[2], score=0.75),
    ]


@pytest.fixture
def sample_search_results():
    """Create sample search results."""
    return [
        SearchResult(
            document_id="doc1",
            text="Python programming guide",
            score=0.95,
            source="vector",
            metadata={"source": "docs"},
        ),
        SearchResult(
            document_id="doc2",
            text="Python best practices",
            score=0.87,
            source="vector",
            metadata={"source": "blog"},
        ),
        SearchResult(
            document_id="doc3",
            text="Python performance tips",
            score=0.75,
            source="vector",
            metadata={"source": "article"},
        ),
    ]


@pytest.mark.asyncio
class TestRerangingService:
    """Test RerangingService functionality."""

    async def test_rerank_empty_results(self, mock_reranker):
        """Test reranking with empty results."""
        service = RerangingService(reranker=mock_reranker)
        result = await service.rerank(
            query="python",
            search_results=[],
            top_k=5,
        )
        assert result == []

    async def test_rerank_converts_and_returns_results(
        self,
        mock_reranker,
        sample_search_results,
    ):
        """Test that reranking converts SearchResult to RetrievedDocument."""
        # Setup reranker to return reranked documents
        reranked_docs = [
            RetrievedDocument(
                id="doc2",
                text="Python best practices",
                score=0.98,  # Updated score
                metadata={"source": "blog"},
            ),
            RetrievedDocument(
                id="doc1",
                text="Python programming guide",
                score=0.93,  # Updated score
                metadata={"source": "docs"},
            ),
        ]
        mock_reranker.rerank.return_value = RerankResult(
            documents=tuple(reranked_docs),
            reranking_time_ms=10.5,
        )

        service = RerangingService(reranker=mock_reranker)
        results = await service.rerank(
            query="python",
            search_results=sample_search_results,
            top_k=2,
        )

        # Verify reranker was called
        mock_reranker.rerank.assert_called_once()
        call_args = mock_reranker.rerank.call_args[0][0]
        assert isinstance(call_args, RerankRequest)
        assert call_args.query == "python"
        assert len(call_args.documents) == 3

        # Verify results are returned with updated scores
        assert len(results) == 2
        assert results[0].document_id == "doc2"
        assert results[0].score == 0.98
        assert results[1].document_id == "doc1"
        assert results[1].score == 0.93

    async def test_rerank_with_metrics(self, mock_reranker, sample_search_results):
        """Test reranking with detailed metrics."""
        reranked_docs = [
            RetrievedDocument(
                id="doc2",
                text="Python best practices",
                score=0.98,
                metadata={"source": "blog"},
            ),
            RetrievedDocument(
                id="doc1",
                text="Python programming guide",
                score=0.93,
                metadata={"source": "docs"},
            ),
        ]
        mock_reranker.rerank.return_value = RerankResult(
            documents=tuple(reranked_docs),
            reranking_time_ms=10.5,
        )

        service = RerangingService(reranker=mock_reranker)
        result = await service.rerank_with_metrics(
            query="python",
            search_results=sample_search_results,
            top_k=2,
        )

        assert "results" in result
        assert "metrics" in result
        assert len(result["results"]) == 2
        assert result["metrics"]["input_count"] == 3
        assert result["metrics"]["output_count"] == 2
        assert result["metrics"]["avg_score_before"] > 0
        assert result["metrics"]["avg_score_after"] > 0
        assert result["metrics"]["score_improvement_percent"] >= 0


@pytest.mark.asyncio
class TestHybridSearchWithReranking:
    """Test HybridSearch with reranking integration."""

    async def test_search_without_reranker(
        self,
        mock_vector_service,
        mock_keyword_search,
        sample_vector_results,
    ):
        """Test hybrid search without reranker (backward compatible)."""
        mock_vector_service.search.return_value = sample_vector_results
        mock_keyword_search.search.return_value = []

        hybrid_search = HybridSearch(
            vector_service=mock_vector_service,
            keyword_search=mock_keyword_search,
            reranker=None,
        )

        results = await hybrid_search.search(
            query="python",
            provider="openai",
            model="text-embedding-3-small",
            top_k=3,
        )

        assert len(results) == 3
        assert results[0].document_id == "doc1"
        assert results[0].source == "vector"

    async def test_search_with_reranker_enabled(
        self,
        mock_vector_service,
        mock_keyword_search,
        mock_reranker,
        sample_vector_results,
    ):
        """Test hybrid search with reranker enabled."""
        mock_vector_service.search.return_value = sample_vector_results
        mock_keyword_search.search.return_value = []

        # Setup reranker response
        reranked_docs = [
            RetrievedDocument(
                id="doc2",
                text="Python best practices",
                score=0.98,
                metadata={"source": "blog"},
            ),
            RetrievedDocument(
                id="doc1",
                text="Python programming guide",
                score=0.95,
                metadata={"source": "docs"},
            ),
            RetrievedDocument(
                id="doc3",
                text="Python performance tips",
                score=0.85,
                metadata={"source": "article"},
            ),
        ]
        mock_reranker.rerank.return_value = RerankResult(
            documents=tuple(reranked_docs),
            reranking_time_ms=15.2,
        )

        hybrid_search = HybridSearch(
            vector_service=mock_vector_service,
            keyword_search=mock_keyword_search,
            reranker=mock_reranker,
        )

        results = await hybrid_search.search(
            query="python",
            provider="openai",
            model="text-embedding-3-small",
            top_k=3,
            enable_reranking=True,
        )

        # Verify reranker was called
        mock_reranker.rerank.assert_called_once()

        # Verify results are reranked
        assert len(results) == 3
        assert results[0].document_id == "doc2"
        assert results[0].score == 0.98
        assert results[1].document_id == "doc1"
        assert results[1].score == 0.95

    async def test_search_with_reranker_disabled(
        self,
        mock_vector_service,
        mock_keyword_search,
        mock_reranker,
        sample_vector_results,
    ):
        """Test hybrid search with reranker disabled despite being configured."""
        mock_vector_service.search.return_value = sample_vector_results
        mock_keyword_search.search.return_value = []

        hybrid_search = HybridSearch(
            vector_service=mock_vector_service,
            keyword_search=mock_keyword_search,
            reranker=mock_reranker,
        )

        results = await hybrid_search.search(
            query="python",
            provider="openai",
            model="text-embedding-3-small",
            top_k=3,
            enable_reranking=False,
        )

        # Verify reranker was not called
        mock_reranker.rerank.assert_not_called()

        # Verify results are from fusion only
        assert len(results) == 3
        assert results[0].document_id == "doc1"

    async def test_search_retrieves_more_candidates_for_reranking(
        self,
        mock_vector_service,
        mock_keyword_search,
        mock_reranker,
        sample_vector_results,
    ):
        """Test that more candidates are retrieved when reranking is enabled."""
        mock_vector_service.search.return_value = sample_vector_results
        mock_keyword_search.search.return_value = []
        mock_reranker.rerank.return_value = RerankResult(
            documents=(
                RetrievedDocument(id="doc1", text="Python programming guide", score=0.95, metadata={}),
                RetrievedDocument(id="doc2", text="Python best practices", score=0.87, metadata={}),
            ),
            reranking_time_ms=5.0,
        )

        hybrid_search = HybridSearch(
            vector_service=mock_vector_service,
            keyword_search=mock_keyword_search,
            reranker=mock_reranker,
        )

        await hybrid_search.search(
            query="python",
            provider="openai",
            model="text-embedding-3-small",
            top_k=2,
            enable_reranking=True,
        )

        # Verify vector search requested more candidates (top_k * 4)
        mock_vector_service.search.assert_called_once()
        call_kwargs = mock_vector_service.search.call_args[1]
        assert call_kwargs["top_k"] == 8  # 2 * 4

    async def test_search_handles_empty_fused_results(
        self,
        mock_vector_service,
        mock_keyword_search,
        mock_reranker,
    ):
        """Test search handles case where fusion returns empty results."""
        mock_vector_service.search.return_value = []
        mock_keyword_search.search.return_value = []

        hybrid_search = HybridSearch(
            vector_service=mock_vector_service,
            keyword_search=mock_keyword_search,
            reranker=mock_reranker,
        )

        results = await hybrid_search.search(
            query="python",
            provider="openai",
            model="text-embedding-3-small",
            top_k=3,
            enable_reranking=True,
        )

        # Verify reranker was not called
        mock_reranker.rerank.assert_not_called()

        # Verify empty results returned
        assert results == []
