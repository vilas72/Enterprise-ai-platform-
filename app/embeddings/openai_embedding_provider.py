from app.clients.openai_client import OpenAIClient
from app.core.config import settings
from app.embeddings.embedding_provider import EmbeddingProvider
from app.embeddings.embedding_request import EmbeddingRequest
from app.embeddings.embedding_response import EmbeddingResponse


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    OpenAI Embedding Provider.
    """

    def __init__(self):
        self.client = OpenAIClient()

    def generate(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:

        model = (
            request.model
            or settings.openai.embedding_model
        )

        response = self.client.generate_embedding(
            request=request,
            model=model,
        )

         
        embedding = response.data[0].embedding
        
        return EmbeddingResponse(
            provider="OpenAI",
            model=model,
            dimensions=len(embedding),
            embedding=embedding,
        )