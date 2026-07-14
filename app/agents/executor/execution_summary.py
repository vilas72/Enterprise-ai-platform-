"""
Agent execution summary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExecutionSummary:
    """
    Summary of an Agent execution.

    Produced by AgentExecutor after the
    execution engine completes.
    """

    success: bool

    executed_steps: int

    failed_steps: int

    skipped_steps: int

    execution_time_ms: float

    output: str = ""

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)