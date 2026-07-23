"""
Enterprise Gateway dependency registration.
"""

from __future__ import annotations

from functools import lru_cache

from app.gateway.gateway import EnterpriseGateway
from app.dependencies.gateway_registry_dependencies import (
    get_gateway_registry,
)
from app.gateway.router import GatewayRouter

from app.dependencies.workflow_dependencies import (
    get_workflow_service,
)

from app.events.dependencies import (
    get_event_publisher,
)

from app.gateway.gateway import EnterpriseGateway

@lru_cache
def get_gateway_router() -> GatewayRouter:
    """
    Create the Enterprise Gateway Router.
    """

    return GatewayRouter(
        registry=get_gateway_registry(),
    )


@lru_cache
def get_enterprise_gateway() -> EnterpriseGateway:
    """
    Create the Enterprise Gateway.
    """

    return EnterpriseGateway(
        registry=get_gateway_registry(),
        workflow_service=get_workflow_service(),
        publisher=get_event_publisher(),
    )

@lru_cache
def get_planner() -> EnterpriseGateway: 
    """
    Create the Enterprise Gateway.
    """

    return EnterpriseGateway(
        registry=get_gateway_registry(),
        workflow_service=get_workflow_service(),
        publisher=get_event_publisher(),
    )