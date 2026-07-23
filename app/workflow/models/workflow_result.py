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

    #
    # Planner / Execution Information
    #

    #
    # Planner / Execution Information
    #

    requested_capability: str | None = Field(
        default=None,
        description="Business capability requested by the caller.",
    )

    workflow_capability: str | None = Field(
        default=None,
        description="Workflow capability selected by the planner.",
    )

    selected_agent: str | None = Field(
        default=None,
        description="Selected business agent.",
    )

    planner: str | None = Field(
        default=None,
        description="Planner used to build the workflow.",
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Planner confidence score.",
    )

    selected_agent: str | None = Field(
        default=None,
        description="Selected business agent.",
    )

    planner: str | None = Field(
        default=None,
        description="Planner used to build the workflow.",
    )

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Planner confidence score.",
    )

    #
    # Result
    #

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
        description="Additional workflow metadata.",
    )

    error: str | None = Field(
        default=None,
        description="Workflow failure reason.",
    )

    #
    # Timing
    #

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
    
    workflow_version: str | None = Field(
        default=None,
        description="Workflow definition version.",
    )