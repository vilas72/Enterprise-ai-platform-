"""
Planner result models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PlannerStep(BaseModel):
    """
    Single workflow execution step.
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
    Output produced by a planner.

    requested_capability:
        Original capability requested by the client.

    workflow_capability:
        Workflow template selected by the planner.
    """

    model_config = ConfigDict(extra="forbid")

    planner: str

    selected_agent: str

    requested_capability: str

    workflow_capability: str

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )

    workflow: list[PlannerStep] = Field(
        default_factory=list,
    )