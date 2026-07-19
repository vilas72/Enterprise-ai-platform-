"""
Workflow Step Models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class WorkflowStepType(str, Enum):
    """
    Supported workflow step types.
    """

    TASK = "task"
    DECISION = "decision"
    PARALLEL = "parallel"
    HUMAN_APPROVAL = "human_approval"
    REFLECTION = "reflection"


class WorkflowStepStatus(str, Enum):
    """
    Runtime workflow step status.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class RetryPolicy(BaseModel):
    """
    Retry configuration for a workflow step.
    """

    max_attempts: int = Field(
        default=1,
        ge=1,
        description="Maximum retry attempts.",
    )

    retry_delay_seconds: int = Field(
        default=0,
        ge=0,
        description="Delay between retries.",
    )


class WorkflowStep(BaseModel):
    """
    Represents a single executable workflow step.
    """

    id: str = Field(
        description="Unique workflow step identifier.",
    )

    name: str = Field(
        description="Human readable step name.",
    )

    description: str | None = Field(
        default=None,
        description="Optional description.",
    )

    type: WorkflowStepType = Field(
        default=WorkflowStepType.TASK,
    )

    agent: str = Field(
        description="Target agent name.",
    )

    capability: str = Field(
        description="Capability executed by the agent.",
    )

    inputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Inputs passed to the agent.",
    )

    outputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Outputs produced after execution.",
    )

    depends_on: list[str] = Field(
        default_factory=list,
        description="Step dependencies.",
    )

    retry_policy: RetryPolicy = Field(
        default_factory=RetryPolicy,
    )

    timeout_seconds: int = Field(
        default=300,
        ge=1,
        description="Execution timeout.",
    )

    status: WorkflowStepStatus = Field(
        default=WorkflowStepStatus.PENDING,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )