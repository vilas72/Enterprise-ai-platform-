"""Base API schemas for Enterprise Agents."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentRequestAPI(BaseModel):
    """Base request model for all Enterprise Agents."""

    capability: str = Field(
        ...,
        description="Business capability to execute.",
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution payload.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional request metadata.",
    )

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )


class AgentResponseAPI(BaseModel):
    """Base response model for all Enterprise Agents."""

    success: bool = Field(
        ...,
        description="Execution status.",
    )
    message: str = Field(
        ...,
        description="Execution message.",
    )
    result: Any | None = Field(
        default=None,
        description="Execution result.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution metadata.",
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

