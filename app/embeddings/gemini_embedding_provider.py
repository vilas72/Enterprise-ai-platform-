from app.clients.gemini_client import GeminiClient
from app.core.config import settings
from app.embeddings.embedding_provider import EmbeddingProvider
from app.embeddings.embedding_request import EmbeddingRequest
from app.embeddings.embedding_response import EmbeddingResponse


class GeminiEmbeddingProvider(EmbeddingProvider):
    """
    Gemini Embedding Provider.
    """

    def __init__(self):
        self.client = GeminiClient()

    def generate(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        model = (
            request.model
            or settings.gemini.embedding_model
        )

        response = self.client.generate_embedding(
            request=request,
            model=model,
        )

        embedding = response.embeddings[0].values

        return EmbeddingResponse(
            provider="Gemini",
            model=model,
            dimensions=len(embedding),
            embedding=embedding,
        )