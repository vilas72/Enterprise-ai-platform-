"""
Planner execution result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.agents.models.agent_plan import AgentPlan


@dataclass(slots=True)
class PlannerResult:
    """
    Result produced by the Planner.
    """

    success: bool

    plan: AgentPlan

    reasoning: str = ""

    confidence: float = 1.0

    metadata: dict[str, Any] | None = None