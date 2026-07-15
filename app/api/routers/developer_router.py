"""
Enterprise Developer Agent API Router.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.developer.dependencies import (
    get_developer_agent,
)
from app.agents.developer.developer_agent import (
    DeveloperAgent,
)
from app.agents.developer.models import (
    DeveloperAgentRequest,
    JiraIssueReference,
    PullRequestReference,
    RepositoryReference,
)

from app.api.schemas.agents.developer_request import (
    DeveloperRequestAPI,
)
from app.api.schemas.agents.developer_response import (
    DeveloperResponseAPI,
)

router = APIRouter(
    prefix="/developer",
    tags=["Developer Agent"],
)

@router.post(
    "/execute",
    response_model=DeveloperResponseAPI,
    status_code=status.HTTP_200_OK,
)
async def execute(
    request: DeveloperRequestAPI,
    developer_agent: DeveloperAgent = Depends(
        get_developer_agent,
    ),
) -> DeveloperResponseAPI:
    """
    Execute a Developer Agent capability.
    """

    try:

        payload = request.payload or {}

        repository = None
        repo_payload = payload.get("repository")
        if isinstance(repo_payload, dict) and repo_payload.get("owner") and repo_payload.get("repository"):
            repository = RepositoryReference(
                owner=repo_payload["owner"],
                repository=repo_payload["repository"],
                branch=repo_payload.get("branch"),
            )

        pull_request = None
        pr_payload = payload.get("pull_request")
        if isinstance(pr_payload, dict) and repository is not None and pr_payload.get("pull_request_number") is not None:
            pull_request = PullRequestReference(
                repository=repository,
                pull_request_number=pr_payload["pull_request_number"],
            )

        jira_issue = None
        jira_payload = payload.get("jira_issue")
        if isinstance(jira_payload, dict) and jira_payload.get("issue_key"):
            jira_issue = JiraIssueReference(issue_key=jira_payload["issue_key"])

        agent_request = DeveloperAgentRequest(
            capability=request.capability,
            metadata=request.metadata,
            query=payload.get("query"),
            code=payload.get("code"),
            path=payload.get("path"),
            title=payload.get("title"),
            description=payload.get("description"),
            repository=repository,
            pull_request=pull_request,
            jira_issue=jira_issue,
        )

        response = await developer_agent.execute(
            agent_request,
        )

        return DeveloperResponseAPI(
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

@router.get(
    "/capabilities",
)
async def capabilities(
    developer_agent: DeveloperAgent = Depends(
        get_developer_agent,
    ),
) -> dict:
    """
    Return supported Developer Agent capabilities.
    """

    return {
        "agent": developer_agent.name,
        "description": developer_agent.description,
        "capabilities": developer_agent.capabilities(),
    }

@router.get(
    "/health",
)
async def health() -> dict:
    """
    Developer Agent health.
    """

    return {
        "status": "UP",
        "agent": "developer",
    }

