from __future__ import annotations

from app.search.keyword_search import KeywordSearch
from app.search.rank_fusion import RankFusion
from app.search.search_result import SearchResult
from app.search.reranking_service import RerangingService
from app.vectorstore.vector_service import VectorService
from app.reranking.reranker import Reranker


class HybridSearch:
    """
    Hybrid search combining vector and keyword search with optional reranking.

    Pipeline:
    1. Vector search (top k*2)
    2. Keyword search (top k*2)
    3. Rank fusion
    4. (Optional) Reranking with ML model
    """

    def __init__(
        self,
        vector_service: VectorService,
        keyword_search: KeywordSearch,
        reranker: Reranker | None = None,
    ):
        self._vector_service = vector_service
        self._keyword_search = keyword_search
        self._rank_fusion = RankFusion()
        self._reranker = reranker
        self._reranking_service = (
            RerangingService(reranker) if reranker else None
        )

    def index(self, documents: list[dict[str, object]]) -> None:
        self._keyword_search.index(documents)

    async def search(
        self,
        query: str,
        provider: str,
        model: str | None,
        top_k: int = 5,
        enable_reranking: bool = True,
    ) -> list[SearchResult]:
        """
        Perform hybrid search with optional reranking.

        Args:
            query: Search query
            provider: Embedding provider
            model: Embedding model
            top_k: Number of results to return
            enable_reranking: Whether to apply reranking if available

        Returns:
            Ranked search results
        """
        # Retrieve more documents for reranking candidates
        search_limit = top_k * 4 if (self._reranker and enable_reranking) else top_k

        # Vector search
        vector_results = self._vector_service.search(
            query=query,
            provider=provider,
            model=model,
            top_k=search_limit,
        )

        # Keyword search
        keyword_results = self._keyword_search.search(
            query=query,
            top_k=search_limit,
        )

        # Convert VectorSearchResult to SearchResult
        converted_vector_results = [
            SearchResult(
                document_id=result.document.id,
                text=result.document.text,
                score=result.score,
                source="vector",
                metadata=result.document.metadata,
            )
            for result in vector_results
        ]

        # Rank fusion
        fused_results = self._rank_fusion.fuse(
            converted_vector_results,
            keyword_results,
        )[:search_limit]

        # Apply reranking if available and enabled
        if self._reranker and enable_reranking and fused_results:
            reranked_results = await self._reranking_service.rerank(
                query=query,
                search_results=fused_results,
                top_k=top_k,
            )
            return reranked_results

        # Return top-k fused results if no reranking
        return fused_results[:top_k]
