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
from app.agents.support.models import SupportAgentRequest
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

    async def execute(
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

        return await handler(request)
    
    async def generate_resolution(
        self,
        request: SupportAgentRequest,
    ) -> str:
        prompt = f"""`
        Generate a production-ready resolution.

        Title:
        {request.title}

        Description:
        {request.description}

        Query:
        {request.query}
        """

        return self._generate(prompt)
    
        
    async def escalation_recommendation(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Generate an escalation recommendation for a support ticket.
        """

        logger.info("Generating escalation recommendation for support ticket.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Generate a professional escalation recommendation for the following support ticket.

            Include:

            - Root cause analysis
            - Recommended next steps
            - References to relevant documentation

            Support Ticket

            {request.description}
            """
        )
        
    async def search_knowledge_base(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Search the knowledge base for relevant articles.
        """

        logger.info("Searching knowledge base for relevant articles.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Search the knowledge base for relevant articles related to the following support ticket.

            Include:

            - Article titles
            - Summaries
            - Links to full articles

            Support Ticket

            {request.description}
            """
        )
        
    async def summarize_incident(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Summarize a support incident.
        """

        logger.info("Summarizing support incident.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Summarize the following support incident.

            Include:

            - Key details
            - Root cause
            - Resolution steps
            - Lessons learned

            Support Incident

            {request.description}
            """
        )
        
    async def similar_incidents(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Find similar support incidents.
        """

        logger.info("Finding similar support incidents.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Find similar support incidents related to the following support ticket.

            Include:

            - Incident summaries
            - Root causes
            - Resolutions
            - Lessons learned

            Support Ticket

            {request.description}
            """
        )
        
    async def recommend_articles(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Recommend knowledge articles for a support ticket.
        """

        logger.info("Recommending knowledge articles for support ticket.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Recommend knowledge articles for the following support ticket.

            Include:

            - Article titles
            - Summaries
            - Links to full articles

            Support Ticket

            {request.description}
            """
        )
    
    async def analyze_root_cause(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Analyze the root cause of a support ticket.
        """

        logger.info("Analyzing root cause of support ticket.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Analyze the root cause of the following support ticket.

            Include:

            - Key details
            - Root cause analysis
            - Recommendations for resolution

            Support Ticket

            {request.description}
            """
        )
    
    async def update_ticket(
        self,
        request: SupportAgentRequest,
    ) -> str:
        """
        Update a support ticket.
        """

        logger.info("Updating support ticket.")

        return await self._generate(
            f"""
            You are a senior software engineer.

            Update the following support ticket with the latest information.

            Include:

            - Updated status
            - Resolution steps
            - References to relevant documentation

            Support Ticket

            {request.description}
            """
        )