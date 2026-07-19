"""
Workflow Definition Models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from app.workflow.models.workflow_step import WorkflowStep


class WorkflowType(str, Enum):
    """
    Supported workflow types.
    """

    SINGLE_AGENT = "single_agent"
    MULTI_AGENT = "multi_agent"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class WorkflowDefinition(BaseModel):
    """
    Defines an executable workflow.
    """

    id: str = Field(
        description="Unique workflow identifier.",
    )

    name: str = Field(
        description="Workflow name.",
    )

    description: str | None = Field(
        default=None,
        description="Workflow description.",
    )

    type: WorkflowType = Field(
        default=WorkflowType.SINGLE_AGENT,
        description="Workflow execution type.",
    )

    version: str = Field(
        default="1.0.0",
        description="Workflow version.",
    )

    steps: list[WorkflowStep] = Field(
        default_factory=list,
        description="Workflow execution steps.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional workflow metadata.",
    )

    enabled: bool = Field(
        default=True,
        description="Whether the workflow is enabled.",
    )

    timeout_seconds: int = Field(
        default=600,
        ge=1,
        description="Workflow timeout.",
    )

    @property
    def step_count(self) -> int:
        """
        Number of workflow steps.
        """

        return len(self.steps)