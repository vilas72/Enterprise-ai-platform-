from app.registry.provider_registry import ProviderRegistry
from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.mock_provider import MockProvider

def register_providers():

    ProviderRegistry.register(
        "openai",
        OpenAIProvider
    )

    ProviderRegistry.register(
        "gemini",
        GeminiProvider
    )
    ProviderRegistry.register("mock", MockProvider)