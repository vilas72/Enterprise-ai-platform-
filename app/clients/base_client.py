from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator

from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse


class BaseClient(ABC):
    """
    Base interface for all AI provider SDK clients.

    Implementations:
        - OpenAIClient
        - GeminiClient
        - BedrockClient
        - AzureOpenAIClient
        - ClaudeClient
    """

    @abstractmethod
    def generate(
        self,
        request: GenerateRequest,
        model: str,
    ) -> GenerateResponse:
        """
        Generate a complete AI response.
        """
        raise NotImplementedError

    @abstractmethod
    def stream(
        self,
        request: GenerateRequest,
        model: str,
    ) -> Generator[str, None, None]:
        """
        Stream AI response chunks.
        """
        raise NotImplementedError