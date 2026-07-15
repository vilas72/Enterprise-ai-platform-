"""
Enterprise Gateway domain models.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GatewayExecutionMode(str, Enum):
    """
    Gateway execution strategy.
    """

    SINGLE_AGENT = "single_agent"
    MULTI_AGENT = "multi_agent"
    WORKFLOW = "workflow"


class GatewayRequest(BaseModel):
    """
    Enterprise Gateway request.
    """

    capability: str

    payload: dict[str, Any] = Field(default_factory=dict)

    execution_mode: GatewayExecutionMode = (
        GatewayExecutionMode.SINGLE_AGENT
    )

    correlation_id: str | None = None

    user_id: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class GatewayExecutionMetadata(BaseModel):
    """
    Gateway execution metadata.
    """

    selected_agent: str | None = None

    execution_mode: GatewayExecutionMode

    governance_approved: bool = False

    execution_started_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    execution_completed_at: datetime | None = None

    execution_time_ms: float | None = None

    additional_metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class GatewayResponse(BaseModel):
    """
    Enterprise Gateway response.
    """

    success: bool

    message: str

    result: Any | None = None

    metadata: GatewayExecutionMetadata