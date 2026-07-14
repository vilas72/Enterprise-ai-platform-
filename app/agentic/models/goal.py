from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.agentic.models.value_objects.execution_constraints import (
    ExecutionConstraints,
)
from app.agentic.models.value_objects.goal_priority import GoalPriority
from app.agentic.models.value_objects.goal_status import GoalStatus
from app.agentic.models.value_objects.objective import Objective
from app.agentic.models.value_objects.success_criteria import SuccessCriteria


class Goal(BaseModel):
    """
    Aggregate Root representing an enterprise business goal.

    A Goal owns its objectives, execution constraints,
    success criteria and lifecycle.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    goal_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    title: str

    description: str | None = None

    status: GoalStatus = GoalStatus.CREATED

    priority: GoalPriority = GoalPriority.NORMAL

    objectives: list[Objective] = Field(
        default_factory=list,
    )

    success_criteria: list[SuccessCriteria] = Field(
        default_factory=list,
    )

    constraints: ExecutionConstraints = Field(
        default_factory=ExecutionConstraints,
    )

    assigned_agents: list[str] = Field(
        default_factory=list,
    )

    progress: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    completed_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Goal title cannot be empty.")

        return value

    @property
    def is_completed(self) -> bool:
        return self.status == GoalStatus.COMPLETED

    @property
    def is_active(self) -> bool:
        return self.status in {
            GoalStatus.PLANNING,
            GoalStatus.EXECUTING,
            GoalStatus.REFLECTING,
            GoalStatus.REPLANNING,
        }

    def add_objective(
        self,
        objective: Objective,
    ) -> None:
        self.objectives.append(objective)
        self.touch()

    def add_success_criteria(
        self,
        criteria: SuccessCriteria,
    ) -> None:
        self.success_criteria.append(criteria)
        self.touch()

    def assign_agent(
        self,
        agent_id: str,
    ) -> None:
        if agent_id not in self.assigned_agents:
            self.assigned_agents.append(agent_id)
            self.touch()

    def update_progress(
        self,
        progress: float,
    ) -> None:
        self.progress = max(0.0, min(progress, 100.0))
        self.touch()

    def mark_planning(self) -> None:
        self.status = GoalStatus.PLANNING
        self.touch()

    def mark_executing(self) -> None:
        self.status = GoalStatus.EXECUTING
        self.touch()

    def mark_reflecting(self) -> None:
        self.status = GoalStatus.REFLECTING
        self.touch()

    def mark_replanning(self) -> None:
        self.status = GoalStatus.REPLANNING
        self.touch()

    def mark_completed(self) -> None:
        self.status = GoalStatus.COMPLETED
        self.progress = 100.0
        self.completed_at = datetime.now(UTC)
        self.touch()

    def mark_failed(self) -> None:
        self.status = GoalStatus.FAILED
        self.touch()

    def cancel(self) -> None:
        self.status = GoalStatus.CANCELLED
        self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)