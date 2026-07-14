"""
Enterprise LLM Planner.
"""

from __future__ import annotations

from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_request import AgentRequest
from app.agents.planner.llm.planner_parser import PlannerParser
from app.agents.planner.llm.planner_prompt import PlannerPrompt
from app.agents.planner.planner import Planner
from app.agents.planner.planner_result import PlannerResult
from app.services.ai_service import AIService


class LLMPlanner(Planner):
    """
    Planner powered by an LLM.

    This implementation will evolve to support
    GPT-5, Claude, Gemini, DeepSeek, etc.
    """

    def __init__(
        self,
        ai_service: AIService,
        parser: PlannerParser,
    ) -> None:

        self._ai_service = ai_service
        self._parser = parser

    def create_plan(
        self,
        request: AgentRequest,
        context: AgentContext,
    ) -> PlannerResult:

        #
        # Next step:
        # Build GenerateRequest
        # Invoke AIService
        # Parse structured response
        #

        raise NotImplementedError(
            "LLM planner integration will be implemented "
            "after tool-aware planning is introduced."
        )