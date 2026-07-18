"""
AI business actions for the Developer Agent.

This module encapsulates AI-powered capabilities used by the
Developer Agent.

Responsibilities
----------------
- Explain code
- Generate unit tests
- Generate documentation
- Architecture recommendations

This layer delegates all AI execution to the Enterprise AIService.
"""

from __future__ import annotations

import logging

from app.agents.developer.models import (
    ArchitectureRecommendation,
    DeveloperAgentRequest,
)
from app.domain.generate_request import GenerateRequest
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)


class AIActions:
    """
    Enterprise AI business actions.

    This class contains AI orchestration only.
    """

    def __init__(
        self,
        ai_service: AIService,
    ) -> None:
        self._ai_service = ai_service

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _require_code(
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Validate source code.
        """

        if request.code:
            return request.code

        # Backward-compatible fallbacks for older caller payloads.
        for key in ("code", "source_code", "content"):
            value = request.metadata.get(key)
            if isinstance(value, str) and value:
                return value

        if request.description:
            return request.description

        raise ValueError("Code is required.")

    def _generate(
        self,
        prompt: str,
    ) -> str:
        """
        Execute an AI generation request.
        """

        response = self._ai_service.generate(
            GenerateRequest(
                prompt=prompt,
            )
        )

        if hasattr(response, "response") and isinstance(response.response, str):
            return response.response

        # Backward compatibility for legacy response contracts.
        if hasattr(response, "text") and isinstance(response.text, str):
            return response.text

        raise ValueError("AI provider returned an unsupported response shape.")

    # ---------------------------------------------------------
    # Explain Code
    # ---------------------------------------------------------

    def explain_code(
        self,
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Explain source code.
        """

        code = self._require_code(request)

        logger.info("Explaining source code.")

        return self._generate(
            f"""
            You are a senior software architect.

            Explain the following source code.

            Include:

            - Purpose
            - Flow
            - Business logic
            - Design patterns
            - Improvements

            Source Code

            {code}
            """
        )

    # ---------------------------------------------------------
    # Unit Tests
    # ---------------------------------------------------------

    def generate_unit_tests(
        self,
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Generate unit tests.
        """

        code = self._require_code(request)

        logger.info("Generating unit tests.")

        return self._generate(
            f"""
            Generate production-quality unit tests.

            Requirements:

            - Happy path
            - Negative scenarios
            - Edge cases
            - Mock external dependencies

            Source Code

            {code}
            """
        )
        
        # ---------------------------------------------------------
    # Documentation
    # ---------------------------------------------------------

    def generate_documentation(
        self,
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Generate technical documentation.
        """

        code = self._require_code(request)

        logger.info("Generating technical documentation.")

        return self._generate(
            f"""
            Generate professional technical documentation for the following code.

            Include:

            - Overview
            - Responsibilities
            - Public APIs
            - Inputs
            - Outputs
            - Dependencies
            - Error Handling
            - Usage Example
            - Best Practices

            Source Code

            {code}
"""
        )

    # ---------------------------------------------------------
    # Architecture Recommendations
    # ---------------------------------------------------------

    def architecture_recommendations(
        self,
        request: DeveloperAgentRequest,
    ) -> list[ArchitectureRecommendation]:
        """
        Generate architecture improvement recommendations.
        """

        code = self._require_code(request)

        logger.info("Generating architecture recommendations.")

        response = self._generate(
            f"""
            You are a Principal Enterprise Architect.

            Review the following implementation.

            Provide architecture recommendations.

            For each recommendation include:

            - Title
            - Description
            - Impact
            - Priority
            - Rationale

            Source Code

            {code}
"""
        )

        return [
            ArchitectureRecommendation(
                title="Architecture Review",
                description=response,
                impact="Medium",
                priority="Medium",
                rationale="Generated by Enterprise AI Service.",
            )
        ]

    # ---------------------------------------------------------
    # Dispatcher
    # ---------------------------------------------------------

    def execute(
        self,
        capability: str,
        request: DeveloperAgentRequest,
    ):
        """
        Execute an AI capability.
        """

        handlers = {
            "explain_code": self.explain_code,
            "generate_unit_tests": self.generate_unit_tests,
            "generate_documentation": self.generate_documentation,
            "architecture_recommendations": self.architecture_recommendations,
        }

        handler = handlers.get(capability)

        if handler is None:
            raise ValueError(
                f"Unsupported AI capability: {capability}"
            )

        return handler(request)