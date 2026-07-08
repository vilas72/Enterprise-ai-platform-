import uuid

from app.embeddings.embedding_request import EmbeddingRequest
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.vector_document import VectorDocument
from app.vectorstore.vector_search_result import VectorSearchResult
from app.vectorstore.vector_store import VectorStore


class VectorService:
    """
    Service responsible for indexing and searching vectors.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    def index(
        self,
        text: str,
        document_id: str | None = None,
        metadata: dict[str, str] | None = None,
        provider: str | None = None,
        model: str | None = None,
    ) -> str:
        """
        Index a document.
        """

        embedding = self._embedding_service.generate(
            EmbeddingRequest(
                text=text,
                provider=provider,
                model=model,
            )
        )

        document = VectorDocument(
            id=document_id or str(uuid.uuid4()),
            text=text,
            embedding=embedding.embedding,
            metadata=metadata or {},
        )

        self._vector_store.index(document)

        return document.id

    def search(
        self,
        query: str,
        top_k: int = 5,
        provider: str | None = None,
        model: str | None = None,
    ) -> list[VectorSearchResult]:
        """
        Search similar documents.
        """

        embedding = self._embedding_service.generate(
            EmbeddingRequest(
                text=query,
                provider=provider,
                model=model,
            )
        )

        return self._vector_store.search(
            embedding=embedding.embedding,
            top_k=top_k,
        )

    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document.
        """

        self._vector_store.delete(document_id)

    def clear(self) -> None:
        """
        Clear all indexed documents.
        """

        self._vector_store.clear()

    def count(self) -> int:
        """
        Return indexed document count.
        """

        return self._vector_store.count()