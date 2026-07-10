"""Reranking service for search result quality improvement."""

from __future__ import annotations

from app.rag.retrieved_document import RetrievedDocument
from app.reranking.reranker import Reranker
from app.reranking.rerank_request import RerankRequest
from app.search.search_result import SearchResult


class RerangingService:
    """
    Service that orchestrates document reranking.

    Handles conversion between SearchResult and RetrievedDocument formats,
    applies reranking strategy, and returns ranked results.
    """

    def __init__(self, reranker: Reranker):
        """
        Initialize the reranking service.

        Args:
            reranker: Reranking strategy implementation
        """
        self._reranker = reranker

    async def rerank(
        self,
        query: str,
        search_results: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Rerank search results based on relevance to query.

        Converts SearchResult objects to RetrievedDocument format,
        applies reranking, and returns top-k results with updated scores.

        Args:
            query: Original user query
            search_results: Initial search results to rerank
            top_k: Number of results to return

        Returns:
            Reranked search results, ordered by relevance score
        """
        if not search_results:
            return []

        # Convert SearchResult to RetrievedDocument format
        documents = tuple(
            RetrievedDocument(
                id=result.document_id,
                text=result.text,
                score=result.score,
                metadata=result.metadata,
            )
            for result in search_results
        )

        # Create rerank request
        rerank_request = RerankRequest(
            query=query,
            documents=documents,
            top_k=top_k,
        )

        # Execute reranking
        rerank_result = await self._reranker.rerank(rerank_request)

        # Create a mapping of document ID to original SearchResult for source preservation
        search_result_map = {
            result.document_id: result
            for result in search_results
        }

        # Convert back to SearchResult with updated scores
        reranked_results = []
        for doc in rerank_result.documents:
            original_result = search_result_map.get(doc.id)
            if original_result:
                reranked_results.append(
                    SearchResult(
                        document_id=doc.id,
                        text=doc.text,
                        score=doc.score,  # Updated by reranker
                        source=original_result.source,  # Preserve original source
                        metadata=doc.metadata,
                    )
                )
        
        return reranked_results

    async def rerank_with_metrics(
        self,
        query: str,
        search_results: list[SearchResult],
        top_k: int = 5,
    ) -> dict:
        """
        Rerank results and return detailed metrics.

        Useful for monitoring reranking effectiveness.

        Args:
            query: Original user query
            search_results: Initial search results
            top_k: Number of results to return

        Returns:
            Dictionary with:
            - results: Reranked SearchResult objects
            - metrics: Reranking statistics
        """
        if not search_results:
            return {
                "results": [],
                "metrics": {
                    "input_count": 0,
                    "output_count": 0,
                    "avg_score_before": 0.0,
                    "avg_score_after": 0.0,
                    "score_improvement": 0.0,
                    "reranking_time_ms": 0.0,
                },
            }

        # Calculate metrics before reranking
        avg_score_before = (
            sum(r.score for r in search_results) / len(search_results)
            if search_results else 0.0
        )

        # Perform reranking
        reranked = await self.rerank(
            query=query,
            search_results=search_results,
            top_k=top_k,
        )

        # Calculate metrics after reranking
        avg_score_after = (
            sum(r.score for r in reranked) / len(reranked)
            if reranked else 0.0
        )

        score_improvement = (
            ((avg_score_after - avg_score_before) / avg_score_before * 100)
            if avg_score_before > 0 else 0.0
        )

        return {
            "results": reranked,
            "metrics": {
                "input_count": len(search_results),
                "output_count": len(reranked),
                "avg_score_before": round(avg_score_before, 4),
                "avg_score_after": round(avg_score_after, 4),
                "score_improvement_percent": round(score_improvement, 2),
            },
        }
