"""
Enterprise Gateway domain models.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
import uuid

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
    
    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
    )
    
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
    
    @classmethod
    def from_workflow(
        cls,
        workflow_result,
        execution_mode: GatewayExecutionMode,
        selected_agent: str | None = None,
        governance_approved: bool = True,
    ):
        return cls(
            selected_agent=selected_agent,
            execution_mode=execution_mode,
            governance_approved=governance_approved,
            execution_completed_at=datetime.utcnow(),
            execution_time_ms=workflow_result.execution_time_ms,
            additional_metadata={
                "workflow_id": workflow_result.workflow_id,
                "execution_id": workflow_result.execution_id,
                "success": workflow_result.success,
            },
        )


class GatewayResponse(BaseModel):
    """
    Enterprise Gateway response.
    """

    success: bool

    message: str

    result: Any | None = None

    metadata: GatewayExecutionMetadata
    
    
    @classmethod
    def from_workflow(
        cls,
        workflow_result,
        metadata,
    ):
        return cls(
            success=workflow_result.success,
            message=getattr(workflow_result, "message", ""),
            result=workflow_result.result,
            metadata=metadata,
        )