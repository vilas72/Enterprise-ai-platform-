from collections.abc import Generator

from app.core.config import settings
from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse
from app.providers.provider_factory import ProviderFactory


class AIService:
    """
    Enterprise AI Service.

    Responsibilities:
    - Resolve provider
    - Delegate request to provider
    """

    def __init__(self, provider_factory: ProviderFactory):
        self.provider_factory = provider_factory

    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:

        provider_name = (
            request.provider
            if request.provider
            else settings.default_provider
        )

        provider = self.provider_factory.create(provider_name)

        return provider.generate(request)

    def stream(
        self,
        request: GenerateRequest,
    ) -> Generator[str, None, None]:
        """
        Stream AI response.
        """

        provider_name = request.provider or settings.default_provider

        provider = self.provider_factory.create(provider_name)

        yield from provider.stream(request)