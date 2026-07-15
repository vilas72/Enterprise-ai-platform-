"""
Enterprise DevOps Agent API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.devops.dependencies import get_devops_agent
from app.agents.devops.devops_agent import DevOpsAgent
from app.agents.devops.models import DevOpsAgentRequest

from app.api.schemas.agents.devops_request import DevOpsRequestAPI
from app.api.schemas.agents.devops_response import DevOpsResponseAPI

router = APIRouter(
    prefix="/devops",
    tags=["DevOps Agent"],
)


@router.post(
    "/execute",
    response_model=DevOpsResponseAPI,
)
async def execute(
    request: DevOpsRequestAPI,
    devops_agent: DevOpsAgent = Depends(
        get_devops_agent,
    ),
) -> DevOpsResponseAPI:

    try:

        payload = request.payload or {}

        agent_request = DevOpsAgentRequest(
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

        response = await devops_agent.execute(
            agent_request,
        )

        return DevOpsResponseAPI(
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
    devops_agent: DevOpsAgent = Depends(
        get_devops_agent,
    ),
):

    return {
        "agent": devops_agent.name,
        "description": devops_agent.description,
        "capabilities": devops_agent.capabilities(),
    }


@router.get("/health")
async def health():

    return {
        "status": "UP",
        "agent": "devops",
    }