"""
Hybrid Search orchestration.

Coordinates enterprise search providers and aggregates
results into a unified response.

This class intentionally contains no search engine specific
implementation.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.knowledge.models import (
    KnowledgeRequest,
    SearchResult,
)


class HybridSearch:
    """
    Enterprise Hybrid Search.

    Responsible only for orchestrating search providers.
    """

    def __init__(
        self,
        search_providers: Sequence,
    ) -> None:
        self._providers = list(search_providers)

    async def search(
        self,
        request: KnowledgeRequest,
    ) -> list[SearchResult]:
        """
        Execute hybrid enterprise search.
        """

        results: list[SearchResult] = []

        for provider in self._providers:
            provider_results = await provider.search(request)
            results.extend(provider_results)

        return self._rank(results)

    @staticmethod
    def _rank(
        results: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Rank search results.

        Current implementation performs score ordering.
        Future versions may delegate to an enterprise reranker.
        """

        return sorted(
            results,
            key=lambda item: item.score,
            reverse=True,
        )