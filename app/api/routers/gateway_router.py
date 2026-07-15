"""
Enterprise Gateway API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.agents.gateway_request import (
    GatewayRequestAPI,
)
from app.api.schemas.agents.gateway_response import (
    GatewayResponseAPI,
)

from app.gateway.dependencies import (
    get_enterprise_gateway,
)

from app.gateway.gateway import EnterpriseGateway
from app.gateway.models import (
    GatewayRequest,
)

router = APIRouter(
    prefix="/gateway",
    tags=["Enterprise Gateway"],
)

@router.post(
            "/execute",
            response_model=GatewayResponseAPI,
            status_code=status.HTTP_200_OK,
        )

async def execute(
    request: GatewayRequestAPI,
    gateway: EnterpriseGateway = Depends(
        get_enterprise_gateway,
    ),
) -> GatewayResponseAPI:
    """
    Execute an enterprise capability.
    """

    try:

        gateway_request = GatewayRequest(
            capability=request.capability,
            execution_mode=request.execution_mode,
            payload=request.payload,
            metadata=request.metadata,
        )

        result = await gateway.execute(
            gateway_request,
        )

        return GatewayResponseAPI(
            success=result.success,
            message=result.message,
            result=result.result,
            metadata=result.metadata.model_dump()
            if result.metadata
            else {},
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    
@router.get(
    "/health",
)

async def health(
    gateway: EnterpriseGateway = Depends(
        get_enterprise_gateway,
    ),
):
    """
    Gateway health.
    """

    return await gateway.health()

@router.get(
    "/capabilities",
)
async def capabilities(
    gateway: EnterpriseGateway = Depends(
        get_enterprise_gateway,
    ),
):
    """
    Supported capabilities.
    """

    return {
        "agents": gateway.supported_agents(),
        "capabilities": gateway.supported_capabilities(),
    }