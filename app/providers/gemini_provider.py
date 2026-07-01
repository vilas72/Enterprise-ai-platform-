from collections.abc import Generator
from time import perf_counter

from app.clients.gemini_client import GeminiClient
from app.core.logging_config import setup_logger
from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse
from app.providers.ai_provider import AIProvider
from app.services.model_resolver import ModelResolver


logger = setup_logger(__name__)


class GeminiProvider(AIProvider):
    """
    Gemini AI Provider.

    Responsibilities:
    - Resolve the model
    - Call the Gemini client
    - Map SDK response to domain response
    """

    def __init__(self):
        self.client = GeminiClient()

    def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:

        start = perf_counter()

        try:

            # Resolve the model (requested or default)
            model_info = ModelResolver.resolve(
                provider="gemini",
                requested_model=request.model,
            )

            # Call Gemini client
            response = self.client.generate(
                request=request,
                model=model_info.name,
            )

            latency = (perf_counter() - start) * 1000

            return GenerateResponse(
                provider="Gemini",
                model=model_info.name,
                response=response.text,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency_ms=latency,
            )

        except Exception:
            logger.exception("Gemini request failed.")
            raise
    
    def stream(
        self,
        request: GenerateRequest,
    ) -> Generator[str, None, None]:
        """
        Stream AI response using Gemini.
        """

        try:

            # Resolve the requested/default model
            model_info = ModelResolver.resolve(
                provider="gemini",
                requested_model=request.model,
            )

            # Delegate streaming to the Gemini client
            yield from self.client.stream(
                request=request,
                model=model_info.name,
            )

        except Exception:
            logger.exception("Gemini streaming failed.")
            raise    