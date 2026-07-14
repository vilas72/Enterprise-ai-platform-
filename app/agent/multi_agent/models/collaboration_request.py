from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.agent.multi_agent.models.agent_descriptor import AgentCapability


class CollaborationRequest(BaseModel):
    """
    Represents a multi-agent collaboration request.

    A collaboration request is the input to the AgentCoordinator.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    collaboration_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    conversation_id: str | None = None

    user_id: str | None = None

    query: str

    preferred_agents: list[str] = Field(
        default_factory=list,
    )

    required_capabilities: frozenset[AgentCapability] = Field(
        default_factory=frozenset,
    )

    context: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    stream: bool = False