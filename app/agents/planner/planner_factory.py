"""
Planner factory.
"""

from __future__ import annotations

from app.agents.planner.planner import Planner
from app.agents.planner.planner_types import PlannerType
from app.agents.planner.rule_based_planner import RuleBasedPlanner
from app.agents.planner.llm.llm_planner import LLMPlanner


class PlannerFactory:
    """
    Planner factory.
    """

    @staticmethod
    def create(
        planner_type: PlannerType,
    ) -> Planner:

        if planner_type == PlannerType.RULE_BASED:
            return RuleBasedPlanner()

        if planner_type == PlannerType.LLM:
            return LLMPlanner()

        if planner_type == PlannerType.HYBRID:
            return RuleBasedPlanner()

        raise ValueError(
            f"Unsupported planner type: {planner_type}"
        )