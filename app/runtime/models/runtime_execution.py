"""
Runtime Execution Models.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.runtime.models.runtime_context import RuntimeContext
from app.runtime.models.runtime_status import (
    RuntimeExecutionMode,
    RuntimeExecutionStatus,
)


class RuntimeExecution(BaseModel):
    """
    Represents a runtime execution instance.
    """

    execution_id: str = Field(
        description="Runtime execution identifier.",
    )

    context: RuntimeContext = Field(
        description="Runtime context.",
    )

    mode: RuntimeExecutionMode = Field(
        default=RuntimeExecutionMode.SYNCHRONOUS,
        description="Execution mode.",
    )

    status: RuntimeExecutionStatus = Field(
        default=RuntimeExecutionStatus.PENDING,
        description="Runtime execution status.",
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
        description="Execution error.",
    )

    @property
    def is_running(self) -> bool:
        """
        Whether execution is running.
        """

        return self.status == RuntimeExecutionStatus.RUNNING

    @property
    def is_completed(self) -> bool:
        """
        Whether execution completed successfully.
        """

        return self.status == RuntimeExecutionStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """
        Whether execution failed.
        """

        return self.status == RuntimeExecutionStatus.FAILED