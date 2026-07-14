from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class ExecutionTrace:
    """
    Represents a single execution trace.
    """

    trace_id: str
    conversation_id: str
    execution_id: str

    component: str
    operation: str

    started_at: datetime
    completed_at: datetime | None = None

    success: bool = True

    duration_ms: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    error: str | None = None


@dataclass(slots=True)
class MetricRecord:
    """
    Runtime metric.
    """

    name: str

    value: float

    timestamp: datetime

    labels: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class RuntimeSnapshot:
    """
    Current runtime statistics.
    """

    timestamp: datetime

    active_conversations: int

    active_agents: int

    active_tools: int

    requests_total: int

    failures_total: int

    average_latency_ms: float
    