
from collections.abc import Generator

from time import perf_counter
from app.clients.openai_client import OpenAIClient
from app.core.logging_config import setup_logger
from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse
from app.providers.ai_provider import AIProvider
from app.services.model_resolver import ModelResolver


logger = setup_logger(__name__)


class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client = OpenAIClient()

    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        """
        Generate an AI response using OpenAI.
        """

        start = perf_counter()

        try:
            # Resolve the model (default or requested)
            model_info = ModelResolver.resolve(
                provider="openai",
                requested_model=request.model,
            )

            # Call the client
            response = self.client.generate(
                request=request,
                model=model_info.name,
            )

            latency = (perf_counter() - start) * 1000

            return GenerateResponse(
                provider="OpenAI",
                model=response.model,
                response=response.choices[0].message.content,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                latency_ms=latency,
                finish_reason="stop",
            )

        except Exception:
            logger.exception("OpenAI request failed.")
            raise
        
    def stream(
        self,
        request: GenerateRequest,
    ) -> Generator[str, None, None]:
        """
        Stream AI response from OpenAI.
        """

        try:

            model_info = ModelResolver.resolve(
                provider="openai",
                requested_model=request.model,
            )

            yield from self.client.stream(
                request=request,
                model=model_info.name,
            )

        except Exception:
            logger.exception("OpenAI streaming failed.")
            raise