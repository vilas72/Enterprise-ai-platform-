"""
Enterprise Planner interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.agents.planner.planner_result import PlannerResult


class Planner(ABC):
    """
    Planner interface.
    """

    @abstractmethod
    async def plan(
        self,
        request: Any,
    ) -> PlannerResult:
        """
        Build an execution plan.
        """

        raise NotImplementedError