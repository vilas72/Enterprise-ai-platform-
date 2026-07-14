from __future__ import annotations

from datetime import datetime, UTC
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.agent.multi_agent.models.agent_descriptor import AgentCapability


class AgentTaskPriority(str, Enum):
    """
    Priority assigned to an agent task.
    """

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AgentTaskStatus(str, Enum):
    """
    Current lifecycle state of a task.
    """

    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentTask(BaseModel):
    """
    Represents a unit of work to be executed by a single agent.

    The Coordinator creates AgentTasks and dispatches them to
    the appropriate agent based on required capabilities.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    task_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique task identifier.",
    )

    title: str = Field(
        description="Short task title.",
    )

    instruction: str = Field(
        description="Instruction for the assigned agent.",
    )

    required_capabilities: frozenset[AgentCapability] = Field(
        default_factory=frozenset,
        description="Capabilities required to execute this task.",
    )

    priority: AgentTaskPriority = AgentTaskPriority.NORMAL

    status: AgentTaskStatus = AgentTaskStatus.PENDING

    assigned_agent_id: str | None = Field(
        default=None,
        description="Identifier of the selected agent.",
    )

    parent_task_id: str | None = Field(
        default=None,
        description="Optional parent task identifier.",
    )

    correlation_id: str | None = Field(
        default=None,
        description="Correlation identifier across collaboration.",
    )

    input_data: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty.")

        return value

    @field_validator("instruction")
    @classmethod
    def validate_instruction(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Task instruction cannot be empty.")

        return value

    @property
    def is_completed(self) -> bool:
        """
        Returns True if the task completed successfully.
        """
        return self.status == AgentTaskStatus.COMPLETED

    @property
    def is_running(self) -> bool:
        """
        Returns True if the task is currently executing.
        """
        return self.status == AgentTaskStatus.RUNNING

    @property
    def is_finished(self) -> bool:
        """
        Returns True if the task reached a terminal state.
        """
        return self.status in {
            AgentTaskStatus.COMPLETED,
            AgentTaskStatus.FAILED,
            AgentTaskStatus.CANCELLED,
        }

    def assign(self, agent_id: str) -> None:
        """
        Assign the task to an agent.
        """
        self.assigned_agent_id = agent_id
        self.status = AgentTaskStatus.ASSIGNED

    def mark_running(self) -> None:
        """
        Mark the task as running.
        """
        self.status = AgentTaskStatus.RUNNING

    def mark_completed(self) -> None:
        """
        Mark the task as completed.
        """
        self.status = AgentTaskStatus.COMPLETED

    def mark_failed(self) -> None:
        """
        Mark the task as failed.
        """
        self.status = AgentTaskStatus.FAILED

    def cancel(self) -> None:
        """
        Cancel the task.
        """
        self.status = AgentTaskStatus.CANCELLED