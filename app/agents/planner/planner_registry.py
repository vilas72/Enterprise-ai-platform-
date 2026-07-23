"""
Planner registry.
"""

from __future__ import annotations

from app.agents.planner.planner import Planner
from app.agents.planner.planner_factory import PlannerFactory
from app.agents.planner.planner_types import PlannerType


class PlannerRegistry:
    """
    Planner registry.
    """

    def __init__(self) -> None:

        self._planners: dict[
            PlannerType,
            Planner,
        ] = {}

    def register(
        self,
        planner_type: PlannerType,
        planner: Planner,
    ) -> None:

        self._planners[planner_type] = planner

    def get(
        self,
        planner_type: PlannerType,
    ) -> Planner:

        planner = self._planners.get(
            planner_type,
        )

        if planner is None:
            planner = PlannerFactory.create(
                planner_type,
            )

            self.register(
                planner_type,
                planner,
            )

        return planner