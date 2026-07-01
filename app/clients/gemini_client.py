from collections.abc import Generator

from google import genai

from app.clients.base_client import BaseClient
from app.core.config import settings
from app.domain.exceptions.ai_provider_exception import AIProviderException
from app.domain.generate_request import GenerateRequest


class GeminiClient(BaseClient):
    """
    Gemini SDK Client.

    Responsible only for communicating with the Gemini SDK.
    """

    def __init__(self):

        provider = settings.gemini

        self.client = genai.Client(
            api_key=provider.api_key,
        )

    def _build_prompt(
        self,
        request: GenerateRequest,
    ) -> str:
        """
        Convert conversation messages into a Gemini prompt.
        """

        prompt_parts = []

        #
        # Add system prompt first.
        #

        if request.system_prompt:
            prompt_parts.append(
                f"System: {request.system_prompt}"
            )

        #
        # Add conversation history.
        #

        for message in request.messages:

            role = message.role.lower()

            if role == "user":
                prompt_parts.append(
                    f"User: {message.content}"
                )

            elif role == "assistant":
                prompt_parts.append(
                    f"Assistant: {message.content}"
                )

            elif role == "system":
                prompt_parts.append(
                    f"System: {message.content}"
                )

            else:
                prompt_parts.append(
                    f"{message.role}: {message.content}"
                )

        return "\n\n".join(prompt_parts)

    def generate(
        self,
        request: GenerateRequest,
        model: str,
    ):

        prompt = self._build_prompt(request)

        try:

            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
            )

            return response

        except Exception as ex:

            message = str(ex)

            if "RESOURCE_EXHAUSTED" in message:
                raise AIProviderException(
                    message="Gemini quota exceeded.",
                    provider="gemini",
                ) from ex

            if "UNAUTHENTICATED" in message:
                raise AIProviderException(
                    message="Gemini authentication failed.",
                    provider="gemini",
                ) from ex

            if "PERMISSION_DENIED" in message:
                raise AIProviderException(
                    message="Gemini permission denied.",
                    provider="gemini",
                ) from ex

            raise AIProviderException(
                message=f"Gemini request failed: {message}",
                provider="gemini",
            ) from ex

    def stream(
        self,
        request: GenerateRequest,
        model: str,
    ) -> Generator[str, None, None]:

        prompt = self._build_prompt(request)

        try:

            stream = self.client.models.generate_content_stream(
                model=model,
                contents=prompt,
            )

            for chunk in stream:

                if chunk.text:
                    yield chunk.text

        except Exception as ex:

            message = str(ex)

            if "RESOURCE_EXHAUSTED" in message:
                raise AIProviderException(
                    message="Gemini quota exceeded.",
                    provider="gemini",
                ) from ex

            if "UNAUTHENTICATED" in message:
                raise AIProviderException(
                    message="Gemini authentication failed.",
                    provider="gemini",
                ) from ex

            if "PERMISSION_DENIED" in message:
                raise AIProviderException(
                    message="Gemini permission denied.",
                    provider="gemini",
                ) from ex

            raise AIProviderException(
                message=f"Gemini streaming failed: {message}",
                provider="gemini",
            ) from ex