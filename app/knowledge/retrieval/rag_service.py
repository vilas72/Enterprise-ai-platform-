"""
Retrieval-Augmented Generation service.
"""

from __future__ import annotations

from app.services.ai_service import AIService
from app.domain.generate_request import GenerateRequest

from app.knowledge.models import (
    KnowledgeRequest,
    KnowledgeResponse,
)

from .retrieval_pipeline import RetrievalPipeline


class RAGService:
    """
    Enterprise RAG orchestration.

    Responsible for:

    - retrieving enterprise context
    - building prompts
    - invoking AIService
    """

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
        ai_service: AIService,
    ) -> None:
        self._retrieval = retrieval_pipeline
        self._ai = ai_service

    async def answer(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:

        results = await self._retrieval.retrieve(request)

        context = "\n\n".join(
            f"{item.title}\n{item.content}"
            for item in results
        )

        prompt = (
            "Use the following enterprise knowledge to answer the question.\n\n"
            f"{context}\n\n"
            f"Question: {request.query}"
        )

        response = self._ai.generate(
            GenerateRequest(
                prompt=prompt,
            )
        )

        return KnowledgeResponse(
            query=request.query,
            answer=response.content,
            results=results,
            citations=[
                result.title
                for result in results
            ],
        )
