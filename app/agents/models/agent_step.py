"""
Agent execution step.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class AgentStepStatus(str, Enum):
    """
    Execution state of an Agent step.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    SKIPPED = "skipped"


@dataclass(slots=True)
class AgentStep:
    """
    Represents one executable step within an Agent plan.
    """

    id: int

    name: str

    description: str

    action: str

    status: AgentStepStatus = AgentStepStatus.PENDING

    result: str = ""

    error: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )