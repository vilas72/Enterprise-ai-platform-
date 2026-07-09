from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from app.domain.value_objects.prompt_context import PromptContext


@dataclass(slots=True)
class ConversationRequest:
    """
    Represents a conversation request entering the AI platform.

    This DTO is transport-agnostic and can be used by:
    - REST API
    - WebSocket
    - CLI
    - MCP
    - Workflow Engine
    - Agent Framework
    """

    # Request Information
    request_id: str = field(default_factory=lambda: str(uuid4()))

    # Conversation
    conversation_id: str = ""
    title: str | None = None

    # User Input
    message: str = ""

    # AI Configuration
    provider: str = ""
    model: str = ""

    # Prompt Configuration
    system_prompt: str | None = None
    prompt_context: PromptContext | None = None

    # Generation Parameters
    temperature: float = 0.7
    max_tokens: int | None = None
    stream: bool = False

    # Feature Flags
    enable_memory: bool = True
    enable_rag: bool = True
    enable_tools: bool = True

    # Identity
    user_id: str | None = None
    session_id: str | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    conversation_metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """
        Validate the request.

        Raises:
            ValueError if any field is invalid.
        """

        self.conversation_id = self.conversation_id.strip()
        self.message = self.message.strip()
        self.provider = self.provider.strip()
        self.model = self.model.strip()

        if not self.conversation_id:
            raise ValueError("conversation_id cannot be empty.")

        if not self.message:
            raise ValueError("message cannot be empty.")

        if not self.provider:
            raise ValueError("provider cannot be empty.")

        if not self.model:
            raise ValueError("model cannot be empty.")

        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError(
                "temperature must be between 0.0 and 2.0."
            )

        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError(
                "max_tokens must be greater than zero."
            )

        if self.title is not None:
            self.title = self.title.strip()