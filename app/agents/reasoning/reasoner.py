"""
Enterprise Reasoner.
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


class Reasoner:
    """
    Coordinates reasoning execution.
    """

    def __init__(
        self,
        strategy: ReasoningStrategy,
    ) -> None:

        self._strategy = strategy

    def reason(
        self,
        request: AgentRequest,
        context: AgentContext,
    ) -> ReasoningResult:

        return self._strategy.reason(
            request,
            context,
        )