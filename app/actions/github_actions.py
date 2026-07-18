"""
GitHub business actions for the Developer Agent.

This module encapsulates GitHub-related business capabilities exposed by
the Developer Agent. It delegates all GitHub operations to the
Enterprise GitHubConnector.

No REST logic should exist in this layer.
"""

from __future__ import annotations

import logging
from typing import Any

from app.agents.developer.models import (
    CodeQualityReport,
    DeveloperAgentRequest,
    RepositoryHealthReport,
    RepositoryReference,
)
from app.connectors.github.github_connector import GitHubConnector

logger = logging.getLogger(__name__)


class GitHubActions:
    """
    GitHub business actions.

    Responsibilities
    ----------------
    • Analyze repository
    • Search repository
    • Create GitHub Issue
    • Review Pull Request
    • Merge Pull Request
    • Repository Health
    • Code Quality
    """

    def __init__(
        self,
        github_connector: GitHubConnector,
    ) -> None:
        self._github = github_connector

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _require_repository(
        request: DeveloperAgentRequest,
    ) -> RepositoryReference:
        """
        Validate repository reference.
        """

        if request.repository is not None:
            return request.repository

        metadata_repository = request.metadata.get("repository")
        if isinstance(metadata_repository, dict):
            owner = metadata_repository.get("owner")
            repository = metadata_repository.get("repository")
            if owner and repository:
                return RepositoryReference(
                    owner=owner,
                    repository=repository,
                    branch=metadata_repository.get("branch"),
                )

        owner = request.metadata.get("owner")
        repository = request.metadata.get("repository")
        if isinstance(owner, str) and isinstance(repository, str):
            return RepositoryReference(
                owner=owner,
                repository=repository,
                branch=request.metadata.get("branch"),
            )

        raise ValueError("Repository is required.")

    @staticmethod
    def _require_query(
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Validate search query.
        """

        if request.query:
            return request.query

        for key in ("query", "search_query", "q"):
            metadata_query = request.metadata.get(key)
            if isinstance(metadata_query, str) and metadata_query:
                return metadata_query

        metadata_payload = request.metadata.get("payload")
        if isinstance(metadata_payload, dict):
            for key in ("query", "search_query", "q"):
                payload_query = metadata_payload.get(key)
                if isinstance(payload_query, str) and payload_query:
                    return payload_query

                if isinstance(payload_query, dict):
                    nested_text = payload_query.get("text")
                    if isinstance(nested_text, str) and nested_text:
                        return nested_text

        raise ValueError("Search query is required.")

    @staticmethod
    def _require_issue_title(
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Validate issue title.
        """

        if request.title:
            return request.title

        metadata_title = request.metadata.get("title")
        if isinstance(metadata_title, str) and metadata_title:
            return metadata_title

        raise ValueError("Issue title is required.")

    # ------------------------------------------------------------------
    # Repository Analysis
    # ------------------------------------------------------------------

    async def analyze_repository(
        self,
        request: DeveloperAgentRequest,
    ) -> dict[str, Any]:
        """
        Analyze a repository.
        """

        repository = self._require_repository(request)

        logger.info(
            "Analyzing repository %s/%s",
            repository.owner,
            repository.repository,
        )

        return await self._github.analyze_repository(
            owner=repository.owner,
            repository=repository.repository,
        )

    async def search_repository(
        self,
        request: DeveloperAgentRequest,
    ) -> list[Any]:
        """
        Search GitHub repositories.
        """

        query = self._require_query(request)

        logger.info(
            "Searching GitHub repositories: %s",
            query,
        )

        return await self._github.search_repositories(
            query=query,
        )

    # ------------------------------------------------------------------
    # GitHub Issues
    # ------------------------------------------------------------------

    async def create_issue(
        self,
        request: DeveloperAgentRequest,
    ) -> Any:
        """
        Create a GitHub issue.
        """

        repository = self._require_repository(request)
        title = self._require_issue_title(request)

        body = request.description
        if not body:
            metadata_description = request.metadata.get("description")
            if isinstance(metadata_description, str):
                body = metadata_description

        logger.info(
            "Creating GitHub issue in %s/%s",
            repository.owner,
            repository.repository,
        )

        return await self._github.create_issue(
            owner=repository.owner,
            repository=repository.repository,
            title=title,
            body=body,
        )

    # ------------------------------------------------------------------
    # Pull Requests
    # ------------------------------------------------------------------

    async def review_pull_request(
        self,
        request: DeveloperAgentRequest,
    ) -> dict[str, Any]:
        """
        Review a pull request.
        """

        if request.pull_request is None:
            raise ValueError("Pull request is required.")

        repository = request.pull_request.repository

        logger.info(
            "Reviewing pull request #%s",
            request.pull_request.pull_request_number,
        )

        return await self._github.review_pull_request(
            owner=repository.owner,
            repository=repository.repository,
            pull_request_number=request.pull_request.pull_request_number,
        )

    async def merge_pull_request(
        self,
        request: DeveloperAgentRequest,
    ) -> bool:
        """
        Merge a pull request.
        """

        if request.pull_request is None:
            raise ValueError("Pull request is required.")

        repository = request.pull_request.repository

        logger.info(
            "Merging pull request #%s",
            request.pull_request.pull_request_number,
        )

        return await self._github.merge_pull_request(
            owner=repository.owner,
            repository=repository.repository,
            pull_request_number=request.pull_request.pull_request_number,
        )
    
        # ------------------------------------------------------------------
    # Repository Health
    # ------------------------------------------------------------------

    async def repository_health(
        self,
        request: DeveloperAgentRequest,
    ) -> RepositoryHealthReport:
        """
        Generate a repository health report.
        """

        repository = self._require_repository(request)

        owner = repository.owner
        logger.info(
            "Generating repository health report for %s/%s",
            owner,
            repository.repository,
        )

        result = await self._github.repository_health(
            owner=owner,
            repository=repository.repository,
        )

        summary = result.get("summary", {})

        return RepositoryHealthReport(
            repository=f"{owner}/{repository.repository}",
            open_pull_requests=summary.get("open_pull_requests", 0),
            open_issues=summary.get("open_issues", 0),
            stale_pull_requests=summary.get(
                "stale_pull_requests",
                0,
            ),
            stale_branches=summary.get(
                "stale_branches",
                0,
            ),
            code_smells=summary.get(
                "code_smells",
                0,
            ),
            documentation_score=summary.get(
                "documentation_score",
            ),
            test_coverage=summary.get(
                "test_coverage",
            ),
            recommendations=result.get(
                "recommendations",
                [],
            ),
        )

    # ------------------------------------------------------------------
    # Code Quality
    # ------------------------------------------------------------------

    async def code_quality(
        self,
        request: DeveloperAgentRequest,
    ) -> CodeQualityReport:
        """
        Generate a code quality assessment.
        """

        repository = self._require_repository(request)

        logger.info(
            "Generating code quality report for %s/%s",
            repository.owner,
            repository.repository,
        )

        result = await self._github.code_quality(
            owner=repository.owner,
            repository=repository.repository,
        )

        return CodeQualityReport(
            score=result.get("score", 0.0),
            strengths=result.get(
                "strengths",
                [],
            ),
            weaknesses=result.get(
                "weaknesses",
                [],
            ),
            recommendations=result.get(
                "recommendations",
                [],
            ),
        )

    # ------------------------------------------------------------------
    # Generic Dispatcher
    # ------------------------------------------------------------------

    async def execute(
        self,
        capability: str,
        request: DeveloperAgentRequest,
    ) -> Any:
        """
        Execute a GitHub capability.

        This method provides a single entry point for the
        DeveloperAgent while keeping GitHub-specific logic inside
        this class.
        """

        handlers = {
            "analyze_repository": self.analyze_repository,
            "search_repository": self.search_repository,
            "create_github_issue": self.create_issue,
            "review_pull_request": self.review_pull_request,
            "merge_pull_request": self.merge_pull_request,
            "repository_health": self.repository_health,
            "code_quality": self.code_quality,
        }

        handler = handlers.get(capability)

        if handler is None:
            raise ValueError(
                f"Unsupported GitHub capability: {capability}"
            )

        return await handler(request)