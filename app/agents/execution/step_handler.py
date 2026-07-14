"""
Base class for execution step handlers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_step import AgentStep


class StepHandler(ABC):
    """
    Base contract for all execution handlers.

    Every handler is responsible for executing one
    specific step type.
    """

    @abstractmethod
    def supports(
        self,
        step: AgentStep,
    ) -> bool:
        """
        Return True if this handler can execute the step.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        step: AgentStep,
        context: AgentContext,
    ) -> None:
        """
        Execute the step.
        """
        raise NotImplementedError