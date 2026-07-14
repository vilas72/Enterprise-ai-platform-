"""
Execution engine result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.agents.models.agent_context import AgentContext


@dataclass(slots=True)
class ExecutionResult:
    """
    Result returned by the execution engine.
    """

    success: bool

    context: AgentContext

    executed_steps: int

    output: str = ""

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)