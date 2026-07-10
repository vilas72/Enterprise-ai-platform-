from __future__ import annotations

from abc import ABC, abstractmethod

from app.reranking.rerank_request import RerankRequest
from app.reranking.rerank_result import RerankResult


class Reranker(ABC):
    """
    Base class for all reranking strategies.
    """

    @abstractmethod
    async def rerank(
        self,
        request: RerankRequest,
    ) -> RerankResult:
        """
        Rerank retrieved documents.
        """
        raise NotImplementedError