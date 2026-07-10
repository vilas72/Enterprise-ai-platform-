from __future__ import annotations

import logging
import time

from app.rag.query_rewriter import QueryRewriter
from app.rag.rag_request import RagRequest
from app.rag.retrieval_result import RetrievalResult
from app.search.hybrid_search import HybridSearch

logger = logging.getLogger(__name__)


class ConversationRetriever:
    """
    Orchestrates the conversation-aware retrieval pipeline.

    Responsibilities:
        - Rewrite conversational queries.
        - Execute hybrid search.
        - Produce a RetrievalResult.
    """

    def __init__(
        self,
        hybrid_search: HybridSearch,
        query_rewriter: QueryRewriter,
    ) -> None:
        self._hybrid_search = hybrid_search
        self._query_rewriter = query_rewriter

    async def retrieve(
        self,
        request: RagRequest,
    ) -> RetrievalResult:
        """
        Execute conversation-aware retrieval.
        """

        start_time = time.perf_counter()

        rewritten_query = await self._query_rewriter.rewrite(request)
        search_request = request.with_query(rewritten_query)
        documents = await self._hybrid_search.search(search_request)

        elapsed = (time.perf_counter() - start_time) * 1000

        logger.debug(
            "Retrieved %d documents in %.2f ms",
            len(documents),
            elapsed,
        )

        return RetrievalResult(
            query=request.query,
            rewritten_query=rewritten_query,
            documents=tuple(documents),
            retrieval_time_ms=elapsed,
            total_candidates=len(documents),
        )
