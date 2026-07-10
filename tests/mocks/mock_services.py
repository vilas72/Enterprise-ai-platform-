"""Mock implementations for testing."""

from typing import Any, Optional
from app.search.search_result import SearchResult
from app.vectorstore.vector_search_result import VectorSearchResult
from app.vectorstore.vector_document import VectorDocument


class MockVectorStore:
    """Mock vector store for testing."""

    def __init__(self) -> None:
        self.documents: dict[str, VectorDocument] = {}

    def index(self, document: VectorDocument) -> None:
        self.documents[document.id] = document

    def search(
        self, embedding: list[float], top_k: int = 5
    ) -> list[VectorSearchResult]:
        """Return mock search results."""
        results = []
        for doc in list(self.documents.values())[:top_k]:
            results.append(
                VectorSearchResult(
                    document=doc,
                    score=0.95 - (len(results) * 0.05),  # Decreasing scores
                )
            )
        return results

    def delete(self, document_id: str) -> None:
        self.documents.pop(document_id, None)

    def clear(self) -> None:
        self.documents.clear()

    def count(self) -> int:
        return len(self.documents)


class MockEmbeddingProvider:
    """Mock embedding provider for testing."""

    async def generate(
        self, text: str, model: str | None = None
    ) -> list[float]:
        """Return mock embedding."""
        # Deterministic mock: hash the text to create consistent embeddings
        hash_val = hash(text) % 1000
        return [float(hash_val) / 1000] * 384  # 384-dim embedding


class MockAIService:
    """Mock AI service for testing."""

    def __init__(self) -> None:
        self.call_count = 0
        self.last_prompt = None

    async def generate(self, request: Any) -> dict:
        """Return mock LLM response."""
        self.call_count += 1
        if request.messages:
            self.last_prompt = request.messages[0].content
        return {
            "response": "This is a mock response from the LLM.",
            "model": "mock-model",
            "tokens_used": 50,
        }


class MockSearchResult:
    """Mock search result for testing."""

    @staticmethod
    def create_mock_results(count: int = 3) -> list[SearchResult]:
        """Create mock search results."""
        results = []
        for i in range(count):
            results.append(
                SearchResult(
                    document_id=f"doc-{i}",
                    text=f"Mock document {i} content",
                    score=0.95 - (i * 0.05),
                    source="mock",
                    metadata={"index": i},
                )
            )
        return results
