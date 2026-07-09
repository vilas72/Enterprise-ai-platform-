from __future__ import annotations

import re
from collections import Counter

from app.search.search_result import SearchResult


class KeywordSearch:
    """
    Lightweight keyword retriever used for lexical search.
    """

    def __init__(self, documents: list[dict[str, object]] | None = None) -> None:
        self._documents = documents or []

    def index(self, documents: list[dict[str, object]]) -> None:
        self._documents = documents

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        if not query.strip():
            return []

        terms = self._tokenize(query)
        if not terms:
            return []

        scored: list[tuple[float, SearchResult]] = []
        for document in self._documents:
            text = str(document.get("text", ""))
            if not text:
                continue

            doc_terms = self._tokenize(text)
            if not doc_terms:
                continue

            overlap = sum(Counter(terms)[term] for term in set(terms) & set(doc_terms))
            if overlap == 0:
                continue

            score = overlap / max(1, len(doc_terms))
            scored.append(
                (
                    score,
                    SearchResult(
                        text=text,
                        score=score,
                        source="keyword",
                        metadata={str(k): str(v) for k, v in dict(document.get("metadata", {})).items()},
                    ),
                )
            )

        scored.sort(key=lambda item: item[0], reverse=True)
        return [result for _, result in scored[:top_k]]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [token for token in re.findall(r"\b[\w']+\b", text.lower()) if token]
