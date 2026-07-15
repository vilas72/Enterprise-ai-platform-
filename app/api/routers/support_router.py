"""
Enterprise Support Agent API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.support.dependencies import get_support_agent
from app.agents.support.models import SupportAgentRequest
from app.agents.support.support_agent import SupportAgent

from app.api.schemas.agents.support_request import SupportRequestAPI
from app.api.schemas.agents.support_response import SupportResponseAPI

router = APIRouter(
    prefix="/support",
    tags=["Support Agent"],
)


@router.post(
    "/execute",
    response_model=SupportResponseAPI,
)
async def execute(
    request: SupportRequestAPI,
    support_agent: SupportAgent = Depends(
        get_support_agent,
    ),
) -> SupportResponseAPI:

    try:

        payload = request.payload or {}

        agent_request = SupportAgentRequest(
            capability=request.capability,
            payload=payload,
            metadata=request.metadata,
            query=payload.get("query"),
            ticket_key=payload.get("ticket_key"),
            project_key=payload.get("project_key"),
        )

        response = await support_agent.execute(
            agent_request,
        )

        return SupportResponseAPI(
            success=response.success,
            message=response.message,
            result=response.result,
            metadata=response.metadata.model_dump()
            if response.metadata
            else {},
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.get("/capabilities")
async def capabilities(
    support_agent: SupportAgent = Depends(
        get_support_agent,
    ),
):

    return {
        "agent": support_agent.name,
        "description": support_agent.description,
        "capabilities": support_agent.capabilities(),
    }


@router.get("/health")
async def health():

    return {
        "status": "UP",
        "agent": "support",
    }