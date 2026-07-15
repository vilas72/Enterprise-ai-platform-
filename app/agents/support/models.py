"""
Enterprise Support Agent domain models.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SupportCapability(str, Enum):
    """
    Supported Support Agent capabilities.
    """

    SEARCH_TICKETS = "search_tickets"

    CREATE_TICKET = "create_ticket"

    UPDATE_TICKET = "update_ticket"

    TRANSITION_TICKET = "transition_ticket"

    SEARCH_KNOWLEDGE = "search_knowledge"

    RECOMMEND_ARTICLES = "recommend_articles"

    SIMILAR_INCIDENTS = "similar_incidents"

    SUMMARIZE_INCIDENT = "summarize_incident"

    GENERATE_RESOLUTION = "generate_resolution"

    ESCALATION_RECOMMENDATION = "escalation_recommendation"


class SupportAgentRequest(BaseModel):
    """
    Support Agent request.
    """

    capability: SupportCapability

    query: str | None = None

    ticket_key: str | None = None

    project_key: str | None = None

    payload: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class SupportExecutionMetadata(BaseModel):
    """
    Execution metadata.
    """

    governance_approved: bool = False

    execution_time_ms: float | None = None

    additional_metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class SupportAgentResponse(BaseModel):
    """
    Support Agent response.
    """

    success: bool

    capability: SupportCapability

    message: str

    result: Any | None = None

    metadata: SupportExecutionMetadata