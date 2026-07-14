"""
Planner response parser.
"""

from __future__ import annotations

import json

from app.agents.models.agent_plan import AgentPlan
from app.agents.models.agent_step import AgentStep
from app.agents.planner.llm.planner_schema import (
    PlannerResponseSchema,
)


class PlannerParser:
    """
    Converts LLM JSON into AgentPlan.
    """

    def parse(
        self,
        response: str,
    ) -> AgentPlan:

        payload = json.loads(response)

        schema = PlannerResponseSchema.model_validate(
            payload
        )

        steps: list[AgentStep] = []

        for index, step in enumerate(
            schema.steps,
            start=1,
        ):

            steps.append(
                AgentStep(
                    id=index,
                    name=step.name,
                    description=step.description,
                    action=step.action,
                )
            )

        return AgentPlan(
            goal="",
            reasoning=schema.reasoning,
            confidence=schema.confidence,
            steps=steps,
        )