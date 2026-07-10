from __future__ import annotations

from dataclasses import dataclass

from app.rag.retrieved_document import RetrievedDocument


@dataclass(slots=True, frozen=True)
class RetrievalResult:
    """Container for retrieval results."""

    query: str
    rewritten_query: str
    documents: tuple[RetrievedDocument, ...]
    retrieval_time_ms: float
    total_candidates: int

    @property
    def document_count(self) -> int:
        return len(self.documents)
