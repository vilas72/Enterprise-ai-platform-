from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentType(str, Enum):
    """
    Supported agent categories.
    """

    PLANNER = "planner"
    REASONER = "reasoner"
    RAG = "rag"
    TOOL = "tool"
    CODE = "code"
    REVIEW = "review"
    SEARCH = "search"
    SQL = "sql"
    CUSTOM = "custom"


class AgentStatus(str, Enum):
    """
    Lifecycle state of an agent.
    """

    ACTIVE = "active"
    DISABLED = "disabled"
    DEPRECATED = "deprecated"


class AgentCapability(str, Enum):
    """
    Capabilities exposed by an agent.

    These capabilities are used by the AgentSelector to determine
    which agents should participate in a collaboration.
    """

    PLANNING = "planning"
    REASONING = "reasoning"
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    TOOL_EXECUTION = "tool_execution"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    SEARCH = "search"
    SQL = "sql"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "classification"
    TRANSLATION = "translation"
    VALIDATION = "validation"


class AgentDescriptor(BaseModel):
    """
    Describes a registered AI agent.

    The descriptor is intentionally execution-agnostic and contains
    only metadata required for discovery, routing, governance,
    and orchestration.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    agent_id: str = Field(
        description="Unique agent identifier."
    )

    name: str = Field(
        description="Human-readable name."
    )

    description: str = Field(
        description="Short description of the agent."
    )

    agent_type: AgentType

    capabilities: frozenset[AgentCapability] = Field(
        default_factory=frozenset
    )

    status: AgentStatus = AgentStatus.ACTIVE

    version: str = "1.0.0"

    priority: int = Field(
        default=100,
        ge=0,
        le=1000,
        description="Lower values indicate higher priority."
    )

    supports_streaming: bool = True

    supports_parallel_execution: bool = True

    max_concurrency: int = Field(
        default=10,
        ge=1,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    tags: frozenset[str] = Field(
        default_factory=frozenset,
    )

    @field_validator("agent_id")
    @classmethod
    def validate_agent_id(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("agent_id cannot be empty.")

        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("name cannot be empty.")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("description cannot be empty.")

        return value

    @property
    def is_active(self) -> bool:
        """
        Returns True when the agent is available for execution.
        """
        return self.status == AgentStatus.ACTIVE

    def supports_capability(
        self,
        capability: AgentCapability,
    ) -> bool:
        """
        Returns True if the agent exposes the requested capability.
        """
        return capability in self.capabilities