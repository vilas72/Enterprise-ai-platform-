from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkflowExecutionStrategy(str, Enum):
    """
    Defines how workflow steps are executed.
    """

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DAG = "dag"
    CONDITIONAL = "conditional"


class WorkflowStatus(str, Enum):
    """
    Workflow lifecycle state.
    """

    DRAFT = "draft"
    ACTIVE = "active"
    DISABLED = "disabled"
    DEPRECATED = "deprecated"


class RetryPolicy(BaseModel):
    """
    Retry configuration for workflow execution.
    """

    model_config = ConfigDict(frozen=True)

    max_attempts: int = Field(
        default=3,
        ge=1,
        le=20,
    )

    backoff_seconds: float = Field(
        default=1.0,
        ge=0,
    )

    exponential_backoff: bool = True


class TimeoutPolicy(BaseModel):
    """
    Timeout configuration.
    """

    model_config = ConfigDict(frozen=True)

    timeout: timedelta = Field(
        default=timedelta(minutes=10),
    )


class ApprovalPolicy(BaseModel):
    """
    Human approval requirements.
    """

    model_config = ConfigDict(frozen=True)

    required: bool = False

    approver_roles: list[str] = Field(
        default_factory=list,
    )


class WorkflowDefinition(BaseModel):
    """
    Aggregate root describing a workflow definition.

    This model is intentionally execution-agnostic and contains only
    declarative workflow configuration.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    workflow_id: str

    name: str

    version: str = "1.0.0"

    description: str | None = None

    status: WorkflowStatus = WorkflowStatus.DRAFT

    strategy: WorkflowExecutionStrategy = (
        WorkflowExecutionStrategy.SEQUENTIAL
    )

    retry_policy: RetryPolicy = Field(
        default_factory=RetryPolicy,
    )

    timeout_policy: TimeoutPolicy = Field(
        default_factory=TimeoutPolicy,
    )

    approval_policy: ApprovalPolicy = Field(
        default_factory=ApprovalPolicy,
    )

    steps: list[Any] = Field(
        default_factory=list,
    )

    variables: dict[str, Any] = Field(
        default_factory=dict,
    )

    output_schema: dict[str, Any] = Field(
        default_factory=dict,
    )

    tags: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    @field_validator("workflow_id")
    @classmethod
    def validate_workflow_id(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("workflow_id cannot be empty.")

        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Workflow name cannot be empty.")

        return value

    @property
    def step_count(self) -> int:
        """
        Returns the number of workflow steps.
        """

        return len(self.steps)

    @property
    def requires_approval(self) -> bool:
        """
        Indicates whether workflow execution requires approval.
        """

        return self.approval_policy.required

    def is_active(self) -> bool:
        """
        Returns True if the workflow can be executed.
        """

        return self.status == WorkflowStatus.ACTIVE

    def add_tag(self, tag: str) -> None:
        """
        Adds a workflow tag.
        """

        tag = tag.strip()

        if tag and tag not in self.tags:
            self.tags.append(tag)

    def add_step(self, step: Any) -> None:
        """
        Adds a workflow step.
        """

        self.steps.append(step)

    def validate_definition(self) -> None:
        """
        Performs semantic validation beyond Pydantic field validation.
        """

        if not self.steps:
            raise ValueError(
                "Workflow must contain at least one step."
            )

        if self.strategy == WorkflowExecutionStrategy.PARALLEL:
            if len(self.steps) < 2:
                raise ValueError(
                    "Parallel workflows require multiple steps."
                )