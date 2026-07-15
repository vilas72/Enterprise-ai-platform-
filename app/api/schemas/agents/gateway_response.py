"""
Gateway response API schema.
"""

from __future__ import annotations

from app.api.schemas.agents.base import AgentResponseAPI


class GatewayResponseAPI(AgentResponseAPI):
    """
    Enterprise Gateway response.
    """
