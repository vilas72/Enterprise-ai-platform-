"""
Runtime Result Models.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class RuntimeResult(BaseModel):
    """
    Result of a runtime execution.
    """

    success: bool = Field(
        description="Whether execution succeeded.",
    )

    execution_id: str = Field(
        description="Runtime execution identifier.",
    )

    agent: str = Field(
        description="Executed agent.",
    )

    capability: str = Field(
        description="Executed capability.",
    )

    result: Any = Field(
        default=None,
        description="Agent execution result.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution metadata.",
    )

    error: str | None = Field(
        default=None,
        description="Execution error.",
    )

    started_at: datetime | None = None

    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    execution_time_ms: float = Field(
        default=0.0,
        ge=0,
    )