"""
Enterprise DevOps Agent domain models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DevOpsCapability(str, Enum):
    """
    Supported DevOps capabilities.
    """

    REPOSITORY_ANALYSIS = "repository_analysis"

    REPOSITORY_HEALTH = "repository_health"

    CODE_QUALITY = "code_quality"

    PULL_REQUEST_REVIEW = "pull_request_review"

    RELEASE_READINESS = "release_readiness"

    INCIDENT_ANALYSIS = "incident_analysis"

    GENERATE_RELEASE_NOTES = "generate_release_notes"

    GENERATE_RUNBOOK = "generate_runbook"

    SUMMARIZE_DEPLOYMENT = "summarize_deployment"


class DevOpsAgentRequest(BaseModel):
    """
    DevOps Agent request.
    """

    capability: DevOpsCapability

    repository: str | None = None

    owner: str | None = None

    pull_request: int | None = None

    issue: str | None = None

    branch: str | None = None

    release: str | None = None

    deployment: str | None = None

    query: str | None = None

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class DevOpsExecutionMetadata(BaseModel):
    """
    Execution metadata.
    """

    governance_approved: bool = False

    execution_time_ms: float | None = None

    additional_metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class DevOpsAgentResponse(BaseModel):
    """
    DevOps Agent response.
    """

    success: bool

    capability: DevOpsCapability

    message: str

    result: Any | None = None

    metadata: DevOpsExecutionMetadata