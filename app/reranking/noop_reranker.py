from __future__ import annotations

import time

from app.reranking.rerank_request import RerankRequest
from app.reranking.rerank_result import RerankResult
from app.reranking.reranker import Reranker


class NoOpReranker(Reranker):
    """
    Default reranker implementation.

    Returns documents unchanged while respecting top_k.
    """

    async def rerank(
        self,
        request: RerankRequest,
    ) -> RerankResult:

        start = time.perf_counter()

        documents = request.documents[: request.top_k]

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return RerankResult(
            documents=documents,
            reranking_time_ms=elapsed,
            metadata={
                "strategy": "noop",
            },
        )