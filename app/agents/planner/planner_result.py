"""
Planner result models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PlannerStep(BaseModel):
    """
    Single execution step.
    """

    model_config = ConfigDict(extra="forbid")

    order: int

    agent: str

    capability: str

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )


class PlannerResult(BaseModel):
    """
    Planner execution result.
    """

    model_config = ConfigDict(extra="forbid")

    planner: str

    selected_agent: str

    capability: str

    confidence: float = Field(
        default=1.0,
        ge=0,
        le=1,
    )

    reasoning: str | None = None

    workflow: list[PlannerStep] = Field(
        default_factory=list,
    )

    requires_reflection: bool = False

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )