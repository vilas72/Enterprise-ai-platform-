"""
Planner response schema.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class PlannerStepSchema(BaseModel):
    """
    Step returned by the LLM planner.
    """

    name: str = Field(...)

    description: str = Field(...)

    action: str = Field(...)


class PlannerResponseSchema(BaseModel):
    """
    Structured response returned by the planner.
    """

    reasoning: str

    confidence: float = 1.0

    steps: list[PlannerStepSchema]