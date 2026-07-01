from app.domain.exceptions.provider_exception import ProviderException
from app.registry.provider_registry import ProviderRegistry


class ProviderFactory:
    """
    Factory responsible for creating AI provider instances.
    """

    @staticmethod
    def create(provider_name: str):

        provider_class = ProviderRegistry.get_provider(provider_name)

        if provider_class is None:
            raise ProviderException(
                message=f"Unsupported provider '{provider_name}'.",
                provider=provider_name,
            )

        return provider_class()