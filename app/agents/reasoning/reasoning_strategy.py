"""
Reasoning strategy contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_request import AgentRequest
from app.agents.reasoning.reasoning_result import (
    ReasoningResult,
)


class ReasoningStrategy(ABC):
    """
    Base contract for all reasoning strategies.
    """

    @abstractmethod
    def reason(
        self,
        request: AgentRequest,
        context: AgentContext,
    ) -> ReasoningResult:
        """
        Perform reasoning.
        """
        raise NotImplementedError