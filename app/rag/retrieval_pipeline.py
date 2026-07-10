from __future__ import annotations

import logging

from app.rag.conversation_retriever import ConversationRetriever
from app.rag.rag_request import RagRequest
from app.rag.retrieval_result import RetrievalResult

logger = logging.getLogger(__name__)


class RetrievalPipeline:
    """Entry point for conversation-aware retrieval."""

    def __init__(
        self,
        conversation_retriever: ConversationRetriever,
    ) -> None:
        self._conversation_retriever = conversation_retriever

    async def retrieve(
        self,
        request: RagRequest,
    ) -> RetrievalResult:
        """Execute the retrieval pipeline."""

        logger.debug(
            "Starting retrieval pipeline for conversation '%s'.",
            request.conversation_id,
        )

        result = await self._conversation_retriever.retrieve(request)

        logger.debug(
            "Retrieval pipeline completed. Documents=%d",
            result.document_count,
        )

        return result
