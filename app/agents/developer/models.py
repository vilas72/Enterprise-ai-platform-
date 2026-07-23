
"""
Developer Agent domain models.

This module defines the request/response contracts exchanged between the
Developer Agent and the rest of the platform.

The models intentionally remain independent from transport protocols
(REST, WebSocket, CLI, etc.) and external connector payloads.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from app.gateway.models import GatewayRequest


class DeveloperCapability(str, Enum):
    """
    Supported business capabilities exposed by the Developer Agent.
    """

    EXPLAIN_CODE = "explain_code"

    ANALYZE_REPOSITORY = "analyze_repository"

    SEARCH_REPOSITORY = "search_repository"

    REVIEW_PULL_REQUEST = "review_pull_request"

    MERGE_PULL_REQUEST = "merge_pull_request"

    CREATE_GITHUB_ISSUE = "create_github_issue"

    GENERATE_UNIT_TESTS = "generate_unit_tests"

    GENERATE_DOCUMENTATION = "generate_documentation"

    REPOSITORY_HEALTH = "repository_health"

    CODE_QUALITY = "code_quality"

    ARCHITECTURE_RECOMMENDATIONS = "architecture_recommendations"

    CREATE_JIRA_BUG = "create_jira_bug"

    CREATE_JIRA_STORY = "create_jira_story"

    TRANSITION_JIRA_ISSUE = "transition_jira_issue"


class RepositoryReference(BaseModel):
    """
    Repository identity.
    """

    model_config = ConfigDict(extra="forbid")

    owner: str = Field(
        ...,
        description="Repository owner or organization.",
    )

    repository: str = Field(
        ...,
        description="Repository name.",
    )

    branch: str | None = Field(
        default=None,
        description="Optional branch.",
    )


class PullRequestReference(BaseModel):
    """
    Pull request reference.
    """

    model_config = ConfigDict(extra="forbid")

    repository: RepositoryReference

    pull_request_number: int = Field(
        ...,
        ge=1,
    )


class JiraIssueReference(BaseModel):
    """
    Jira issue identifier.
    """

    model_config = ConfigDict(extra="forbid")

    issue_key: str
   
    

class DeveloperAgentRequest(BaseModel):
    """
    Generic request accepted by the Developer Agent.
    """

    model_config = ConfigDict(extra="forbid")

    capability: DeveloperCapability

    conversation_id: str | None = None

    repository: RepositoryReference | None = None

    pull_request: PullRequestReference | None = None

    jira_issue: JiraIssueReference | None = None

    query: str | None = None

    code: str | None = None

    path: str | None = None

    title: str | None = None

    description: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    project_key: str | None = None
    
    transition_id: str | None = None
    
    description: str | None = None
    
    @classmethod
    def build_request(
        cls,
        gateway_request: GatewayRequest,
        capability: str,
    ) -> Self:
        payload = gateway_request.payload or {}

        repository = None
        if "repository" in payload:
            repository = RepositoryReference.model_validate(
                payload["repository"]
            )

        pull_request = None
        if "pull_request" in payload:
            pull_request = PullRequestReference.model_validate(
                payload["pull_request"]
            )

        jira_issue = None
        if "jira_issue" in payload:
            jira_issue = JiraIssueReference.model_validate(
                payload["jira_issue"]
            )

        return cls(
            capability=DeveloperCapability(capability),
            conversation_id=gateway_request.request_id,
            repository=repository,
            pull_request=pull_request,
            jira_issue=jira_issue,
            query=payload.get("query"),
            code=payload.get("code"),
            path=payload.get("path"),
            title=payload.get("title"),
            description=payload.get("description"),
            project_key=payload.get("project_key"),
            transition_id=payload.get("transition_id"),
            metadata=gateway_request.metadata,
        )

class DeveloperExecutionMetadata(BaseModel):
    """
    Execution metadata produced by the Developer Agent.
    """

    model_config = ConfigDict(extra="forbid")

    planner: str | None = None

    reasoner: str | None = None

    execution_id: str | None = None

    duration_ms: float | None = None

    reflected: bool = False

    governance_approved: bool | None = None


class DeveloperAgentResponse(BaseModel):
    """
    Business response returned by the Developer Agent.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool

    capability: DeveloperCapability

    message: str

    result: Any | None = None

    metadata: DeveloperExecutionMetadata = Field(
        default_factory=DeveloperExecutionMetadata,
    )


class RepositoryHealthReport(BaseModel):
    """
    Repository health summary.
    """

    model_config = ConfigDict(extra="forbid")

    repository: str

    open_pull_requests: int = 0

    open_issues: int = 0

    stale_pull_requests: int = 0

    stale_branches: int = 0

    code_smells: int = 0

    documentation_score: float | None = None

    test_coverage: float | None = None

    recommendations: list[str] = Field(
        default_factory=list,
    )


class CodeQualityReport(BaseModel):
    """
    Code quality assessment.
    """

    model_config = ConfigDict(extra="forbid")

    score: float

    strengths: list[str] = Field(
        default_factory=list,
    )

    weaknesses: list[str] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )


class ArchitectureRecommendation(BaseModel):
    """
    Architecture improvement recommendation.
    """

    model_config = ConfigDict(extra="forbid")

    title: str

    description: str

    impact: str

    priority: str

    rationale: str