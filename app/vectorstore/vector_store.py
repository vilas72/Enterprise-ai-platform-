from abc import ABC, abstractmethod

from app.vectorstore.vector_document import VectorDocument
from app.vectorstore.vector_search_result import VectorSearchResult


class VectorStore(ABC):
    """
    Base interface for vector stores.
    """

    @abstractmethod
    def index(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Store a document.
        """
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        """
        Search similar documents.
        """
        pass

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Delete a document.
        """
        pass

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove all documents.
        """
        pass

    @abstractmethod
    def count(
        self,
    ) -> int:
        """
        Return number of indexed documents.
        """
        pass