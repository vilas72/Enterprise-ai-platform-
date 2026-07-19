"""
Planner structured output schema.
"""

from __future__ import annotations

from pydantic import BaseModel


class PlannerSchema(BaseModel):

    agent: str

    capability: str

    confidence: float

    reasoning: str