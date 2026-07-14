"""
Agent request domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class AgentRequest:
    """
    Represents an execution request submitted to an Agent.

    This is the root contract for every Agent execution and remains
    independent from any specific LLM provider, workflow engine,
    LangGraph, or MCP implementation.

    Examples
    --------
    - General chat
    - Code generation
    - GitHub repository analysis
    - SQL query execution
    - Enterprise workflow
    - Multi-step reasoning
    """

    #
    # Request Identity
    #

    request_id: str = field(default_factory=lambda: str(uuid4()))

    correlation_id: str | None = None

    conversation_id: str | None = None

    user_id: str | None = None

    tenant_id: str | None = None

    #
    # Agent Information
    #

    agent_name: str = "default"

    #
    # User Task
    #

    task: str = ""

    query: str = ""

    #
    # Execution Context
    #

    context: dict[str, Any] = field(default_factory=dict)

    #
    # Runtime Parameters
    #

    parameters: dict[str, Any] = field(default_factory=dict)

    #
    # Memory
    #

    enable_memory: bool = True

    #
    # Knowledge Retrieval
    #

    enable_rag: bool = True

    #
    # Tool Calling
    #

    enable_tools: bool = True

    allowed_tools: tuple[str, ...] = ()

    #
    # Planning
    #

    enable_planning: bool = True

    max_steps: int = 10

    #
    # Workflow
    #

    workflow_name: str | None = None

    #
    # Provider Overrides
    #

    provider: str | None = None

    model: str | None = None

    temperature: float | None = None

    #
    # Metadata
    #

    metadata: dict[str, Any] = field(default_factory=dict)