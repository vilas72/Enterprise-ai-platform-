from app.core.config import settings
from app.embeddings.embedding_factory import EmbeddingFactory
from app.embeddings.embedding_request import EmbeddingRequest
from app.embeddings.embedding_response import EmbeddingResponse


class EmbeddingService:
    """
    Service responsible for generating embeddings.
    """

    def __init__(
        self,
        embedding_factory: EmbeddingFactory,
    ):
        self._factory = embedding_factory

    def generate(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        provider_name = (
            request.provider
            if request.provider
            else settings.default_provider
        )

        provider = self._factory.create(
            provider_name
        )

        return provider.generate(
            request
        )