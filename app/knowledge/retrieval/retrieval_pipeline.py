"""
Enterprise Retrieval Pipeline.
"""

from __future__ import annotations

from app.agents.knowledge.models import (
    KnowledgeRequest,
    SearchResult,
)

from .hybrid_search import HybridSearch


class RetrievalPipeline:
    """
    Coordinates enterprise retrieval workflow.
    """

    def __init__(
        self,
        hybrid_search: HybridSearch,
        reranker: object | None = None,
        rag_service: object | None = None,
    ) -> None:
        # Keep optional arguments for backward compatibility with older wiring.
        self._hybrid = hybrid_search
        self._reranker = reranker
        self._rag = rag_service

    async def retrieve(
        self,
        request: KnowledgeRequest,
    ) -> list[SearchResult]:
        """
        Execute enterprise retrieval.
        """

        results = await self._hybrid.search(request)

        # Optional reranker integration if a compatible implementation is injected.
        if self._reranker is not None and hasattr(self._reranker, "rerank"):
            rerank_fn = getattr(self._reranker, "rerank")
            reranked = rerank_fn(request.query, results)
            if isinstance(reranked, list):
                return reranked

        return results