from __future__ import annotations

from datetime import timedelta

from pydantic import BaseModel, ConfigDict, Field


class ExecutionConstraints(BaseModel):
    """
    Constraints governing Goal execution.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    max_execution_time: timedelta = Field(
        default=timedelta(minutes=30),
    )

    max_retries: int = Field(
        default=3,
        ge=0,
    )

    allow_parallel_execution: bool = True

    require_human_approval: bool = False

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )