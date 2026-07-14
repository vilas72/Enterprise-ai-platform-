from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CollaborationStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"


class CollaborationResult(BaseModel):
    """
    Result produced by one agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    task_id: str

    agent_id: str

    status: CollaborationStatus

    output: Any = None

    reasoning: str | None = None

    tool_calls: list[str] = Field(
        default_factory=list,
    )

    token_usage: int = 0

    execution_time_ms: float = 0.0

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )