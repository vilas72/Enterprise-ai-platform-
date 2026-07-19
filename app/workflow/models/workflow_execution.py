"""
Workflow Execution Models.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.workflow.models.workflow_context import WorkflowContext
from app.workflow.models.workflow_definition import WorkflowDefinition



class WorkflowExecutionStatus(str, Enum):
    """
    Workflow execution status.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowExecution(BaseModel):
    """
    Represents a workflow execution instance.
    """

    execution_id: str = Field(
        description="Unique workflow execution identifier.",
    )

    workflow: WorkflowDefinition = Field(
        description="Workflow definition.",
    )

    context: WorkflowContext = Field(
        description="Workflow execution context.",
    )

    status: WorkflowExecutionStatus = Field(
        default=WorkflowExecutionStatus.PENDING,
        description="Current execution status.",
    )

    current_step: str | None = Field(
        default=None,
        description="Current executing workflow step.",
    )

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Execution start time.",
    )

    completed_at: datetime | None = Field(
        default=None,
        description="Execution completion time.",
    )

    error: str | None = Field(
        default=None,
        description="Execution failure reason.",
    )

    @property
    def is_completed(self) -> bool:
        """
        Whether workflow execution has completed.
        """

        return self.status == WorkflowExecutionStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """
        Whether workflow execution failed.
        """

        return self.status == WorkflowExecutionStatus.FAILED

    @property
    def total_steps(self) -> int:
        """
        Total number of workflow steps.
        """

        return len(self.workflow.steps)

    @property
    def completed_steps(self) -> int:
        """
        Number of completed workflow steps.
        """

        return len(
            [
                step
                for step in self.workflow.steps
                if step.status.value == "completed"
            ]
        )

    @property
    def progress_percentage(self) -> float:
        """
        Workflow completion percentage.
        """

        if self.total_steps == 0:
            return 100.0

        return round(
            (self.completed_steps / self.total_steps) * 100,
            2,
        )