"""
Gateway request API schema.
"""

from __future__ import annotations

from pydantic import Field

from app.api.schemas.agents.base import AgentRequestAPI
from app.gateway.models import GatewayExecutionMode


class GatewayRequestAPI(AgentRequestAPI):
    """
    Enterprise Gateway request.
    """

    execution_mode: GatewayExecutionMode = Field(
        default=GatewayExecutionMode.SINGLE_AGENT
    )
