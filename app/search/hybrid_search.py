from __future__ import annotations

from app.search.keyword_search import KeywordSearch
from app.search.rank_fusion import RankFusion
from app.search.search_result import SearchResult
from app.vectorstore.vector_service import VectorService


class HybridSearch:

    def __init__(
        self,
        vector_service: VectorService,
        keyword_search: KeywordSearch,
    ):
        self._vector_service = vector_service
        self._keyword_search = keyword_search
        self._rank_fusion = RankFusion()

    def index(self, documents: list[dict[str, object]]) -> None:
        self._keyword_search.index(documents)

    def search(
        self,
        query: str,
        provider: str,
        model: str | None,
        top_k: int = 5,
    ) -> list[SearchResult]:

        vector_results = self._vector_service.search(
            query=query,
            provider=provider,
            model=model,
            top_k=top_k,
        )

        keyword_results = self._keyword_search.search(
            query=query,
            top_k=top_k,
        )

        return self._rank_fusion.fuse(
            vector_results,
            keyword_results,
        )[:top_k]
