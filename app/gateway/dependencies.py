"""
Enterprise Gateway dependency registration.
"""

from __future__ import annotations

from functools import lru_cache

from app.agents.developer.dependencies import get_developer_agent
from app.agents.knowledge.dependencies import get_knowledge_agent
from app.agents.support.dependencies import get_support_agent
from app.agents.devops.dependencies import get_devops_agent

from app.gateway.gateway import EnterpriseGateway
from app.gateway.registry import GatewayRegistry
from app.gateway.router import GatewayRouter


@lru_cache
def get_gateway_registry() -> GatewayRegistry:
    """
    Create and populate the gateway registry.
    """

    registry = GatewayRegistry()

    registry.register(
        "developer",
        get_developer_agent(),
    )

    registry.register(
        "knowledge",
        get_knowledge_agent(),
    )

    registry.register(
        "support",
        get_support_agent(),
    )
    
    registry.register(
        "devops",
        get_devops_agent(),
    )

    return registry


@lru_cache
def get_gateway_router() -> GatewayRouter:
    """
    Create the enterprise gateway router.
    """

    return GatewayRouter(registry=get_gateway_registry())


@lru_cache
def get_enterprise_gateway() -> EnterpriseGateway:
    """
    Create the Enterprise Gateway.
    """

    return EnterpriseGateway(router=get_gateway_router())