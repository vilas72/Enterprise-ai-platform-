"""
Agent execution plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.agents.models.agent_step import AgentStep


@dataclass(slots=True)
class AgentPlan:
    """
    Execution plan produced by the Planner.
    """

    goal: str

    steps: list[AgentStep] = field(
        default_factory=list
    )

    reasoning: str = ""

    confidence: float = 1.0

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def is_empty(self) -> bool:
        return not self.steps