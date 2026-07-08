from app.core.constants import ProviderName
from app.embeddings.embedding_provider import EmbeddingProvider
from app.embeddings.gemini_embedding_provider import GeminiEmbeddingProvider
from app.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider


class EmbeddingFactory:
    """
    Factory responsible for creating embedding providers.
    """

    @staticmethod
    def create(
        provider: ProviderName | str,
    ) -> EmbeddingProvider:

        provider = ProviderName(provider)

        if provider == ProviderName.OPENAI:
            return OpenAIEmbeddingProvider()

        if provider == ProviderName.GEMINI:
            return GeminiEmbeddingProvider()

        raise ValueError(
            f"Embedding provider '{provider}' is not supported."
        )