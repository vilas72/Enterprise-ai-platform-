from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.agent.multi_agent.models.collaboration_result import (
    CollaborationResult,
    CollaborationStatus,
)


class TeamResult(BaseModel):
    """
    Aggregated result returned by the AgentCoordinator.

    This represents the combined output of all participating agents.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    collaboration_id: str

    status: CollaborationStatus

    final_output: str

    results: list[CollaborationResult] = Field(
        default_factory=list,
    )

    total_agents: int = 0

    successful_agents: int = 0

    failed_agents: int = 0

    execution_time_ms: float = 0.0

    total_tokens: int = 0

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )

    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    @property
    def success_rate(self) -> float:
        if self.total_agents == 0:
            return 0.0

        return self.successful_agents / self.total_agents