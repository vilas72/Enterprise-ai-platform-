from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider

class ProviderRegistry:
    _providers = {}

    @classmethod
    def register(cls, name, provider):

        cls._providers[name.lower()] = provider

    @classmethod
    def get_provider(cls, name):

        provider = cls._providers.get(name.lower())

        if provider is None:
            raise ValueError(
                f"{name} provider not registered."
            )

        return provider