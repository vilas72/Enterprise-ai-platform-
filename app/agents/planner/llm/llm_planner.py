"""
LLM Planner.
"""

from __future__ import annotations

import logging
from typing import Any

from app.agents.planner.planner import Planner
from app.agents.planner.planner_result import PlannerResult
from app.agents.planner.rule_based_planner import (
    RuleBasedPlanner,
)

logger = logging.getLogger(__name__)


class LLMPlanner(Planner):
    """
    Enterprise LLM Planner.

    Currently falls back to the rule-based planner.
    """

    def __init__(self) -> None:
        self._fallback = RuleBasedPlanner()

    async def plan(
        self,
        request: Any,
    ) -> PlannerResult:

        logger.info(
            "LLM planner invoked. Using rule-based fallback."
        )

        # TODO
        # Replace with AI Runtime
        # OpenAI
        # Azure OpenAI
        # Anthropic
        # Gemini

        return await self._fallback.plan(request)