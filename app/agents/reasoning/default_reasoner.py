"""
Default deterministic reasoner.
"""

from __future__ import annotations

from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_request import AgentRequest
from app.agents.reasoning.reasoning_result import (
    ReasoningResult,
)
from app.agents.reasoning.reasoning_strategy import (
    ReasoningStrategy,
)


class DefaultReasoner(
    ReasoningStrategy,
):
    """
    Initial deterministic reasoning strategy.

    Future versions will be replaced with
    GPT-5, Claude, Gemini reasoning.
    """

    def reason(
        self,
        request: AgentRequest,
        context: AgentContext,
    ) -> ReasoningResult:

        reasoning = (
            "Execute planner output "
            "using configured runtime."
        )

        return ReasoningResult(
            success=True,
            reasoning=reasoning,
            confidence=1.0,
        )