"""
Planner types.
"""

from __future__ import annotations

from enum import Enum


class PlannerType(str, Enum):
    """
    Supported planner implementations.
    """

    RULE_BASED = "rule_based"

    LLM = "llm"

    HYBRID = "hybrid"