"""
Agent response domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentResponse:
    """
    Represents the final response returned by an Agent.

    This model is provider-independent and workflow-independent.
    It is the unified output contract for all agent executions.
    """

    #
    # Request Identity
    #

    request_id: str

    correlation_id: str | None = None

    conversation_id: str | None = None

    #
    # Execution Status
    #

    success: bool = True

    message: str = ""

    error: str | None = None

    #
    # Generated Output
    #

    output: str = ""

    #
    # Planning
    #

    steps_executed: int = 0

    total_steps: int = 0

    #
    # Tool Execution
    #

    tools_used: tuple[str, ...] = ()

    #
    # Knowledge
    #

    documents_retrieved: int = 0

    #
    # Token Usage
    #

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    #
    # Performance
    #

    execution_time_ms: float = 0.0

    #
    # Metadata
    #

    metadata: dict[str, Any] = field(default_factory=dict)