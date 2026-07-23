from functools import lru_cache

from app.agents.planner.planner import Planner
from app.agents.planner.planner_registry import PlannerRegistry
from app.agents.planner.planner_types import PlannerType


@lru_cache
def get_planner() -> Planner:
    registry = PlannerRegistry()
    return registry.get(PlannerType.RULE_BASED)