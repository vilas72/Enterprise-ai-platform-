"""
Enterprise Knowledge Agent API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.knowledge.dependencies import get_knowledge_agent
from app.agents.knowledge.knowledge_agent import KnowledgeAgent
from app.agents.knowledge.models import KnowledgeAgentRequest

from app.api.schemas.agents.knowledge_request import KnowledgeRequestAPI
from app.api.schemas.agents.knowledge_response import KnowledgeResponseAPI

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Agent"],
)


@router.post(
    "/execute",
    response_model=KnowledgeResponseAPI,
    status_code=status.HTTP_200_OK,
)
async def execute(
    request: KnowledgeRequestAPI,
    knowledge_agent: KnowledgeAgent = Depends(
        get_knowledge_agent,
    ),
) -> KnowledgeResponseAPI:
    """
    Execute a Knowledge Agent capability.
    """

    try:

        payload = request.payload or {}

        agent_request = KnowledgeAgentRequest(
            capability=request.capability,
            query=payload.get("query") or request.metadata.get("query") or "query",
            source=payload.get("source", "all"),
            top_k=payload.get("top_k", 5),
            filters=payload.get("filters", {}),
        )

        response = await knowledge_agent.execute(
            agent_request,
        )

        return KnowledgeResponseAPI(
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
    knowledge_agent: KnowledgeAgent = Depends(
        get_knowledge_agent,
    ),
) -> dict:

    return {
        "agent": knowledge_agent.name,
        "description": knowledge_agent.description,
        "capabilities": knowledge_agent.capabilities(),
    }


@router.get("/health")
async def health() -> dict:

    return {
        "status": "UP",
        "agent": "knowledge",
    }
    
