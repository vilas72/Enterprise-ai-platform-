from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.rag.retrieved_document import RetrievedDocument


@dataclass(slots=True, frozen=True)
class RerankResult:
    """
    Result returned by a reranker.
    """

    documents: tuple[RetrievedDocument, ...]

    reranking_time_ms: float

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def is_empty(self) -> bool:
        return not self.documents