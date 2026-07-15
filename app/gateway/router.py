"""
Enterprise Gateway Router.
"""

from __future__ import annotations

import logging
from typing import Any

from app.agents.developer.models import DeveloperAgentRequest
from app.agents.devops.models import DevOpsAgentRequest
from app.agents.knowledge.models import KnowledgeAgentRequest
from app.agents.support.models import SupportAgentRequest
from app.gateway.exceptions import (
    UnsupportedCapabilityError,
)
from app.gateway.models import (
    GatewayRequest,
)
from app.gateway.registry import (
    GatewayRegistry,
)

logger = logging.getLogger(__name__)


class GatewayRouter:
    """
    Responsible for selecting the appropriate
    business agent.
    """

    def __init__(
        self,
        registry: GatewayRegistry,
    ) -> None:

        self._registry = registry

    async def route(
        self,
        request: GatewayRequest,
    ) -> Any:
        """
        Resolve an agent for the request.
        """

        logger.info(
            "Routing capability '%s'.",
            request.capability,
        )

        try:

            return self._registry.find_by_capability(
                request.capability,
            )

        except Exception as exc:

            raise UnsupportedCapabilityError(
                f"No agent found for "
                f"'{request.capability}'."
            ) from exc

    def registered_agents(
        self,
    ) -> list[str]:
        """
        List registered agents.
        """

        return self._registry.names()

    def supported_capabilities(
        self,
    ) -> dict[str, list[str]]:
        """
        Return all supported capabilities.
        """

        return self._registry.supported_capabilities()
    
    def build_agent_request(
        self,
        agent: Any,
        request: GatewayRequest
    ) -> Any:
        """
        Build an agent-specific request from the GatewayRequest.
        """

        payload = request.payload or {}

        agent_name = getattr(agent, "name", "")

        if agent_name == "developer":
            return DeveloperAgentRequest(
                capability=request.capability,
                metadata={**request.metadata, **payload},
                query=payload.get("query"),
                title=payload.get("title"),
                description=payload.get("description"),
            )

        if agent_name == "knowledge":
            return KnowledgeAgentRequest(
                capability=request.capability,
                query=payload.get("query") or request.metadata.get("query") or "query",
                source=payload.get("source", "all"),
                top_k=payload.get("top_k", 5),
                filters=payload.get("filters", {}),
            )

        if agent_name == "support":
            return SupportAgentRequest(
                capability=request.capability,
                payload=payload,
                metadata=request.metadata,
                query=payload.get("query"),
                ticket_key=payload.get("ticket_key"),
                project_key=payload.get("project_key"),
            )

        if agent_name == "devops":
            return DevOpsAgentRequest(
                capability=request.capability,
                payload=payload,
                metadata=request.metadata,
                owner=payload.get("owner"),
                repository=payload.get("repository"),
                pull_request=payload.get("pull_request"),
                issue=payload.get("issue"),
                branch=payload.get("branch"),
                release=payload.get("release"),
                deployment=payload.get("deployment"),
                query=payload.get("query"),
            )

        return payload