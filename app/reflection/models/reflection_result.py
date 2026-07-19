"""
Reflection Result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.reflection.models.reflection_status import (
    ReflectionDecision,
)


@dataclass(slots=True)
class ReflectionResult:
    """
    Reflection result.
    """

    success: bool

    decision: ReflectionDecision

    confidence: float = 1.0

    reason: str | None = None

    recommendations: list[str] = field(
        default_factory=list,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    started_at: datetime | None = None

    completed_at: datetime | None = None

    execution_time_ms: float | None = None