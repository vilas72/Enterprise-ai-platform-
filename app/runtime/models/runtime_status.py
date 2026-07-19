"""
Runtime Status Models.
"""

from __future__ import annotations

from enum import Enum


class RuntimeExecutionStatus(str, Enum):
    """
    Runtime execution status.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class RuntimeExecutionMode(str, Enum):
    """
    Runtime execution mode.
    """

    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    PARALLEL = "parallel"