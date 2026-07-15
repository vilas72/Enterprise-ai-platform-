"""
Knowledge Agent business actions.

This module encapsulates enterprise knowledge business operations and
delegates execution to the Knowledge Runtime.

The Knowledge Agent should never interact directly with retrieval,
AI services, or enterprise connectors.
"""

from __future__ import annotations

import logging

from app.agents.knowledge.models import (
    KnowledgeRequest,
    KnowledgeResponse,
)
from app.knowledge.runtime.knowledge_runtime import KnowledgeRuntime

logger = logging.getLogger(__name__)


class KnowledgeActions:
    """
    Enterprise Knowledge business actions.

    Responsibilities
    ----------------
    - Enterprise Search
    - Semantic Search
    - RAG Question Answering
    - Document Summarization
    - Knowledge Recommendation

    This class intentionally contains no retrieval or AI logic.
    """

    def __init__(
        self,
        knowledge_runtime: KnowledgeRuntime,
    ) -> None:
        self._knowledge_runtime = knowledge_runtime

    async def search(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Execute enterprise knowledge search.
        """

        logger.debug(
            "Executing enterprise search: %s",
            request.query,
        )

        return await self._knowledge_runtime.search(request)

    async def answer(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Execute Retrieval-Augmented Generation.
        """

        logger.debug(
            "Executing enterprise RAG: %s",
            request.query,
        )

        return await self._knowledge_runtime.answer(request)

    async def summarize(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Summarize enterprise knowledge.
        """

        logger.debug(
            "Summarizing knowledge for: %s",
            request.query,
        )

        return await self._knowledge_runtime.summarize(request)

    async def recommend(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResponse:
        """
        Recommend enterprise knowledge.
        """

        logger.debug(
            "Generating recommendations for: %s",
            request.query,
        )

        return await self._knowledge_runtime.recommend(request)