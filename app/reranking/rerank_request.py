from __future__ import annotations

from dataclasses import dataclass

from app.rag.retrieved_document import RetrievedDocument


@dataclass(slots=True, frozen=True)
class RerankRequest:
    """
    Request object for document reranking.

    Encapsulates the original query together with the retrieved
    candidate documents that should be reordered.
    """

    query: str

    documents: tuple[RetrievedDocument, ...]

    top_k: int = 10