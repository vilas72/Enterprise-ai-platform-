"""
Agent execution context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.models.chat_message import ChatMessage
from app.rag.retrieved_document import RetrievedDocument


@dataclass(slots=True)
class AgentContext:
    """
    Shared execution context for an Agent.

    This object is enriched throughout the execution lifecycle and is
    passed between the Planner, Executor, Tool Runtime, Workflow Engine,
    LangGraph adapter, and MCP runtime.
    """

    #
    # Conversation
    #

    conversation_id: str | None = None

    user_id: str | None = None

    tenant_id: str | None = None

    #
    # Conversation Memory
    #

    messages: list[ChatMessage] = field(default_factory=list)

    #
    # Retrieved Knowledge
    #

    retrieved_documents: list[RetrievedDocument] = field(
        default_factory=list
    )

    #
    # Tool Results
    #

    tool_results: dict[str, Any] = field(
        default_factory=dict
    )

    #
    # Workflow State
    #

    variables: dict[str, Any] = field(
        default_factory=dict
    )

    #
    # Runtime Metadata
    #

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def has_memory(self) -> bool:
        return bool(self.messages)

    @property
    def has_documents(self) -> bool:
        return bool(self.retrieved_documents)

    @property
    def has_tool_results(self) -> bool:
        return bool(self.tool_results)