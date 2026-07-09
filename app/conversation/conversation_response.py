from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.conversation.conversation_message import ConversationMessage


@dataclass(slots=True)
class TokenUsage:
    """
    Represents token usage for an AI generation.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass(slots=True)
class RetrievedDocument:
    """
    Represents a document retrieved from the RAG pipeline.
    """

    document_id: str
    chunk_id: str
    score: float
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ToolExecutionResult:
    """
    Represents the execution result of a tool.
    """

    tool_name: str
    success: bool
    output: Any = None
    error: str | None = None
    execution_time_ms: float | None = None


@dataclass(slots=True)
class ConversationResponse:
    """
    Canonical response returned by the ConversationOrchestrator.
    """

    request_id: str

    conversation_id: str

    message: ConversationMessage

    provider: str

    model: str

    usage: TokenUsage = field(default_factory=TokenUsage)

    finish_reason: str | None = None

    latency_ms: float | None = None

    streamed: bool = False

    memory_updated: bool = False

    rag_documents: list[RetrievedDocument] = field(
        default_factory=list
    )

    tool_results: list[ToolExecutionResult] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def content(self) -> str:
        return self.message.content

    @property
    def total_tokens(self) -> int:
        return self.usage.total_tokens