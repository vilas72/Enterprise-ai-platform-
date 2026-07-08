from app.api.schemas.embedding.embedding_request_api import (
    EmbeddingRequestApi,
)
from app.api.schemas.embedding.embedding_response_api import (
    EmbeddingResponseApi,
)
from app.embeddings.embedding_request import EmbeddingRequest
from app.embeddings.embedding_response import EmbeddingResponse


class EmbeddingMapper:

    @staticmethod
    def to_domain(
        request: EmbeddingRequestApi,
    ) -> EmbeddingRequest:

        return EmbeddingRequest(
            text=request.text,
            provider=request.provider,
            model=request.model,
        )

    @staticmethod
    def to_api(
        response: EmbeddingResponse,
    ) -> EmbeddingResponseApi:

        return EmbeddingResponseApi(
            provider=response.provider,
            model=response.model,
            dimensions=response.dimensions,
            embedding=response.embedding,
        )