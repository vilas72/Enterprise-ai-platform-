"""
Enterprise Knowledge Runtime.

Provides the public interface for enterprise knowledge capabilities.
The runtime orchestrates retrieval and AI generation while remaining
agnostic of connector implementations.
"""

from __future__ import annotations

from app.services.ai_service import AIService
from app.agents.knowledge.models import (
    KnowledgeRequest,
    KnowledgeResponse,
)

from app.knowledge.retrieval.hybrid_search import HybridSearch
from app.knowledge.retrieval.rag_service import RAGService
from app.knowledge.retrieval.retrieval_pipeline import RetrievalPipeline


class KnowledgeRuntime:
    """
    Enterprise Knowledge Runtime.

    Coordinates enterprise knowledge operations.

    Responsibilities:
        - Enterprise Search
        - Semantic Search
        - RAG Answering
        - Document Summarization
        - Knowledge Recommendations
    """

    def __init__(
        self,
        ai_service: AIService,
        hybrid_search: HybridSearch,
    ) -> None:
        self._retrieval = RetrievalPipeline(
            hybrid_search=hybrid_search,
        )

        self._rag = RAGService(
            retrieval_pipeline=self._retrieval,
            ai_service=ai_service,
        )

    async def search(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Execute enterprise knowledge search.
        """

        results = await self._retrieval.retrieve(request)

        return KnowledgeResponse(
            query=request.query,
            results=results,
            metadata={
                "operation": "search",
                "total_results": len(results),
            },
        )

    async def answer(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Execute Retrieval-Augmented Generation.
        """

        return await self._rag.answer(request)

    async def summarize(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Generate a summarized response.
        """

        response = await self._rag.answer(request)

        response.metadata["operation"] = "summarize"

        return response

    async def recommend(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Recommend relevant enterprise knowledge.
        """

        response = await self.search(request)

        response.metadata["operation"] = "recommend"

        return response
