from __future__ import annotations

from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_service import VectorService


class SemanticMemory:
    """Placeholder semantic memory component."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_service: VectorService,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_service = vector_service

    async def retrieve(self, conversation_id: str) -> list[str]:
        return []
