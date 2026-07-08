from collections.abc import Generator

from openai import (
    APIConnectionError,
    AuthenticationError,
    BadRequestError,
    OpenAI,
    RateLimitError,
)

from app.clients.base_client import BaseClient
from app.core.config import settings
from app.domain.exceptions.ai_provider_exception import AIProviderException
from app.domain.generate_request import GenerateRequest

from app.embeddings.embedding_request import EmbeddingRequest


class OpenAIClient(BaseClient):
    """
    OpenAI SDK Client.

    Responsible only for communicating with the OpenAI SDK.
    """

    def __init__(self):

        provider = settings.openai

        self.client = OpenAI(
            api_key=provider.api_key,
            base_url=provider.base_url or None,
        )
       

    def _build_messages(
        self,
        request: GenerateRequest,
    ) -> list[dict]:
        """
        Convert domain messages into the format expected by OpenAI.
        """

        messages = []

        #
        # Add system prompt first if present.
        #

        if request.system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": request.system_prompt,
                }
            )

        #
        # Add conversation history.
        #

        messages.extend(
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        )

        return messages

    def generate(
        self,
        request: GenerateRequest,
        model: str,
    ):

        messages = self._build_messages(request)

        try:
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            return response

        except AuthenticationError as ex:
            raise AIProviderException(
                message="OpenAI authentication failed.",
                provider="openai",
            ) from ex

        except RateLimitError as ex:
            raise AIProviderException(
                message="OpenAI quota exceeded.",
                provider="openai",
            ) from ex

        except APIConnectionError as ex:
            raise AIProviderException(
                message="Unable to connect to OpenAI.",
                provider="openai",
            ) from ex

        except BadRequestError as ex:
            raise AIProviderException(
                message=f"Invalid OpenAI request: {ex}",
                provider="openai",
            ) from ex

    def stream(
        self,
        request: GenerateRequest,
        model: str,
    ) -> Generator[str, None, None]:

        messages = self._build_messages(request)

        try:

            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            )

            for chunk in stream:

                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):
                    yield chunk.choices[0].delta.content

        except AuthenticationError as ex:
            raise AIProviderException(
                message="OpenAI authentication failed.",
                provider="openai",
            ) from ex

        except RateLimitError as ex:
            raise AIProviderException(
                message="OpenAI quota exceeded.",
                provider="openai",
            ) from ex

        except APIConnectionError as ex:
            raise AIProviderException(
                message="Unable to connect to OpenAI.",
                provider="openai",
            ) from ex

        except BadRequestError as ex:
            raise AIProviderException(
                message=f"Invalid OpenAI request: {ex}",
                provider="openai",
            ) from ex
            
    def generate_embedding(
    self,
    request: EmbeddingRequest,
    model: str,
    ):
        """
        Generate embedding using OpenAI.
        """

        try:

            response = self.client.embeddings.create(
                model=model,
                input=request.text,
            )

            return response

        except AuthenticationError as ex:
            raise AIProviderException(
                message="OpenAI authentication failed.",
                provider="openai",
            ) from ex

        except RateLimitError as ex:

            message = str(ex)

            if "rate_limit_exceeded" in message:
                raise AIProviderException(
                    message="OpenAI rate limit exceeded. Reduce max_tokens or context size.",
                    provider="openai",
                ) from ex

            if "insufficient_quota" in message:
                raise AIProviderException(
                    message="OpenAI billing quota exceeded.",
                    provider="openai",
                ) from ex

            raise AIProviderException(
                message=message,
                provider="openai",
            ) from ex

        except APIConnectionError as ex:
            raise AIProviderException(
                message="Unable to connect to OpenAI.",
                provider="openai",
            ) from ex

        except BadRequestError as ex:
            raise AIProviderException(
                message=f"Invalid OpenAI request: {ex}",
                provider="openai",
            ) from ex        