"""
Reasoning result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ReasoningResult:
    """
    Result of agent reasoning.
    """

    success: bool

    reasoning: str

    confidence: float = 1.0

    metadata: dict[str, Any] = field(default_factory=dict)