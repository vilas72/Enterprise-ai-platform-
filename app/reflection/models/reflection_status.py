"""
Reflection Status.
"""

from __future__ import annotations

from enum import Enum


class ReflectionStatus(str, Enum):
    """
    Reflection execution status.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    SKIPPED = "skipped"


class ReflectionDecision(str, Enum):
    """
    Reflection outcome.
    """

    CONTINUE = "continue"

    RETRY = "retry"

    ESCALATE = "escalate"

    HUMAN_APPROVAL = "human_approval"

    TERMINATE = "terminate"