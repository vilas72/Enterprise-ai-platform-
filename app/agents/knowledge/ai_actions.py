"""
Knowledge Agent AI actions.

This module encapsulates AI-specific capabilities used by the
Knowledge Agent. It delegates all LLM interactions to the existing
Enterprise AIService.
"""

from __future__ import annotations

import logging

from app.services.ai_service import AIService
from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse

logger = logging.getLogger(__name__)


class AIActions:
    """
    AI actions for the Knowledge Agent.

    Responsibilities
    ----------------
    - Text summarization
    - Knowledge explanation
    - Answer refinement
    - Generic AI generation

    This class intentionally contains no retrieval,
    connector, or business logic.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        self._ai_service = ai_service

    async def generate(
        self,
        request: GenerateRequest,
    ) -> GenerateResponse:
        """
        Generate an AI response.
        """

        logger.debug("Generating AI response.")

        return self._ai_service.generate(request)

    async def summarize(
        self,
        text: str,
    ) -> GenerateResponse:
        """
        Summarize enterprise documentation.
        """

        prompt = (
            "Summarize the following enterprise documentation.\n\n"
            f"{text}"
        )

        logger.debug("Summarizing enterprise content.")

        return self._ai_service.generate(
            GenerateRequest(
                prompt=prompt,
            )
        )

    async def explain(
        self,
        text: str,
    ) -> GenerateResponse:
        """
        Explain technical documentation.
        """

        prompt = (
            "Explain the following content in a clear and concise manner.\n\n"
            f"{text}"
        )

        logger.debug("Explaining enterprise content.")

        return self._ai_service.generate(
            GenerateRequest(
                prompt=prompt,
            )
        )

    async def rewrite(
        self,
        text: str,
    ) -> GenerateResponse:
        """
        Rewrite enterprise documentation.
        """

        prompt = (
            "Rewrite the following content while preserving its meaning.\n\n"
            f"{text}"
        )

        logger.debug("Rewriting enterprise content.")

        return self._ai_service.generate(
            GenerateRequest(
                prompt=prompt,
            )
        )