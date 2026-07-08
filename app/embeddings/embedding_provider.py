from abc import ABC, abstractmethod

from app.embeddings.embedding_request import EmbeddingRequest
from app.embeddings.embedding_response import EmbeddingResponse


class EmbeddingProvider(ABC):
    """
    Base interface for embedding providers.
    """

    @abstractmethod
    def generate(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate embedding for the supplied text.
        """
        pass