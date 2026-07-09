from __future__ import annotations

from app.search.search_result import SearchResult


class RankFusion:
    """
    Simple reciprocal-rank fusion for combining multiple result lists.
    """

    def fuse(self, *result_lists: list[SearchResult]) -> list[SearchResult]:
        ranked: dict[str, tuple[float, SearchResult]] = {}

        for result_list in result_lists:
            for rank, result in enumerate(result_list):
                key = result.document_id
                if key not in ranked:
                    ranked[key] = (0.0, result)
                reciprocal_rank = 1.0 / (rank + 60.0)
                current_score, current_result = ranked[key]
                ranked[key] = (current_score + reciprocal_rank, current_result)

        combined = sorted(ranked.values(), key=lambda item: item[0], reverse=True)
        return [result for _, result in combined]
