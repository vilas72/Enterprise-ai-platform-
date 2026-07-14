"""
Enterprise Agent Planner.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_request import AgentRequest
from app.agents.planner.planner_result import PlannerResult


class Planner(ABC):
    """
    Responsible for converting a user request into
    an executable AgentPlan.

    Future implementations:

    - RuleBasedPlanner
    - LLMPlanner
    - WorkflowPlanner
    - LangGraphPlanner
    """

    @abstractmethod
    def create_plan(
        self,
        request: AgentRequest,
        context: AgentContext,
    ) -> PlannerResult:
        """
        Produce an execution plan.
        """
        raise NotImplementedError