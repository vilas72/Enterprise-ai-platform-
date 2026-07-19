"""
Workflow Result Models.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class WorkflowResult(BaseModel):
    """
    Result of a workflow execution.
    """

    success: bool = Field(
        description="Whether the workflow completed successfully.",
    )

    workflow_id: str = Field(
        description="Workflow identifier.",
    )

    execution_id: str = Field(
        description="Workflow execution identifier.",
    )

    result: Any = Field(
        default=None,
        description="Final workflow result.",
    )

    step_results: dict[str, Any] = Field(
        default_factory=dict,
        description="Results from all executed workflow steps.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Workflow execution metadata.",
    )

    error: str | None = Field(
        default=None,
        description="Workflow failure reason.",
    )

    started_at: datetime | None = Field(
        default=None,
        description="Workflow start time.",
    )

    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Workflow completion time.",
    )

    execution_time_ms: float = Field(
        default=0.0,
        ge=0,
        description="Workflow execution time in milliseconds.",
    )