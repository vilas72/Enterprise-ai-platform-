from collections.abc import Generator

from httpx import request

from app.core.config import settings
from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse
from app.providers.provider_factory import ProviderFactory

from app.tracking.cost_calculator import CostCalculator
from app.tracking.usage_mapper import UsageMapper
from app.tracking.usage_tracker import UsageTracker

from app.prompt.prompt_service import PromptService

class AIService:
    """
    Enterprise AI Service.

    Responsibilities:
    - Resolve provider
    - Delegate request to provider
    """

    def __init__(self, provider_factory: ProviderFactory, usage_tracker: UsageTracker,prompt_service: PromptService):
        self.provider_factory = provider_factory
        self.usage_tracker = usage_tracker
        self.prompt_service = prompt_service
    
    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:

        self._prepare_prompt(request)
        
        provider_name = (
            request.provider
            if request.provider
            else settings.default_provider
        )

        provider = self.provider_factory.create(provider_name)

        response = provider.generate(request)
        usage = UsageMapper.from_generate_response(response)
        usage.estimated_cost = CostCalculator.calculate(usage)
        self.usage_tracker.track(usage)

        return response

    def stream(
        self,
        request: GenerateRequest,
    ) -> Generator[str, None, None]:
        """
        Stream AI response.
        """
        self._prepare_prompt(request)
        
        provider_name = request.provider or settings.default_provider

        provider = self.provider_factory.create(provider_name)

        yield from provider.stream(request)
        
    def _prepare_prompt(
    self,
    request: GenerateRequest,
) -> None:
        """
        Render prompt template if PromptContext is provided.
        """

        if request.prompt_context:
            request.prompt = self.prompt_service.render_prompt(
                name=request.prompt_context.name,
                variables=request.prompt_context.variables,
            )    