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
        metadata = request.metadata or {}

        repository = None
        repo_payload = payload.get("repository")
        if isinstance(repo_payload, dict) and repo_payload.get("owner") and repo_payload.get("repository"):
            repository = RepositoryReference(
                owner=repo_payload["owner"],
                repository=repo_payload["repository"],
                branch=repo_payload.get("branch"),
            )
        elif payload.get("owner") and payload.get("repository"):
            repository = RepositoryReference(
                owner=payload["owner"],
                repository=payload["repository"],
                branch=payload.get("branch"),
            )
        elif isinstance(metadata.get("repository"), dict):
            metadata_repository = metadata["repository"]
            if metadata_repository.get("owner") and metadata_repository.get("repository"):
                repository = RepositoryReference(
                    owner=metadata_repository["owner"],
                    repository=metadata_repository["repository"],
                    branch=metadata_repository.get("branch"),
                )
        elif metadata.get("owner") and metadata.get("repository"):
            repository = RepositoryReference(
                owner=metadata["owner"],
                repository=metadata["repository"],
                branch=metadata.get("branch"),
            )

        pull_request = None
        pr_payload = payload.get("pull_request")
        if isinstance(pr_payload, dict) and repository is not None and pr_payload.get("pull_request_number") is not None:
            pull_request = PullRequestReference(
                repository=repository,
                pull_request_number=pr_payload["pull_request_number"],
            )
        elif repository is not None and payload.get("pull_request_number") is not None:
            pull_request = PullRequestReference(
                repository=repository,
                pull_request_number=payload["pull_request_number"],
            )

        jira_issue = None
        jira_payload = payload.get("jira_issue")
        if isinstance(jira_payload, dict) and jira_payload.get("issue_key"):
            jira_issue = JiraIssueReference(issue_key=jira_payload["issue_key"])

        agent_request = DeveloperAgentRequest(
            capability=request.capability,
            metadata=request.metadata,
            query=(
                payload.get("query")
                or payload.get("search_query")
                or payload.get("q")
                or metadata.get("query")
                or metadata.get("search_query")
                or metadata.get("q")
            ),
            code=payload.get("code") or metadata.get("code"),
            path=payload.get("path"),
            title=payload.get("title") or metadata.get("title"),
            description=payload.get("description") or metadata.get("description"),
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

@router.get("/capabilities")
async def capabilities(
    developer_agent: DeveloperAgent = Depends(
        get_developer_agent,
    ),
) -> dict:

    return {
        "agent": "developer",
        "description": "Developer Agent",
        "capabilities": [
            capability.value
            if hasattr(capability, "value")
            else str(capability)
            for capability in developer_agent.supported_capabilities
        ],
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

