"""
Planner parser.
"""

from __future__ import annotations

from app.agents.planner.llm.planner_schema import (
    PlannerSchema,
)
from app.agents.planner.planner_result import (
    PlannerResult,
    PlannerStep,
)


class PlannerParser:
    """
    Converts LLM output into PlannerResult.
    """

    @staticmethod
    def parse(
        schema: PlannerSchema,
    ) -> PlannerResult:

        return PlannerResult(
            planner="llm",
            selected_agent=schema.agent,
            capability=schema.capability,
            confidence=schema.confidence,
            reasoning=schema.reasoning,
            workflow=[
                PlannerStep(
                    order=1,
                    agent=schema.agent,
                    capability=schema.capability,
                )
            ],
        )