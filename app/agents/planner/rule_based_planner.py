"""
Default rule-based planner implementation.
"""

from __future__ import annotations

from app.agents.models.agent_context import AgentContext
from app.agents.models.agent_plan import AgentPlan
from app.agents.models.agent_request import AgentRequest
from app.agents.models.agent_step import AgentStep
from app.agents.planner.planner import Planner
from app.agents.planner.planner_result import PlannerResult


class RuleBasedPlanner(Planner):
    """
    Default deterministic planner.

    Produces a simple execution plan without requiring an LLM.
    This implementation serves as the baseline planner and can
    later be replaced by LLMPlanner or LangGraphPlanner.
    """

    def create_plan(
        self,
        request: AgentRequest,
        context: AgentContext,
    ) -> PlannerResult:

        steps: list[AgentStep] = []

        steps.append(
            AgentStep(
                id=1,
                name="Understand Request",
                description="Analyse the user request.",
                action="reason",
            )
        )

        if request.enable_rag:

            steps.append(
                AgentStep(
                    id=2,
                    name="Retrieve Knowledge",
                    description="Retrieve enterprise knowledge.",
                    action="retrieve",
                )
            )

        if request.enable_tools:

            steps.append(
                AgentStep(
                    id=len(steps) + 1,
                    name="Execute Tools",
                    description="Execute required tools.",
                    action="tools",
                )
            )

        steps.append(
            AgentStep(
                id=len(steps) + 1,
                name="Generate Response",
                description="Generate the final response.",
                action="generate",
            )
        )

        plan = AgentPlan(
            goal=request.task,
            steps=steps,
            reasoning="Rule-based execution plan.",
            confidence=1.0,
        )

        return PlannerResult(
            success=True,
            plan=plan,
            reasoning="Deterministic planner executed successfully.",
            confidence=1.0,
        )