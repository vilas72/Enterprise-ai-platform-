from __future__ import annotations

from datetime import datetime
from typing import Any

from app.connectors.github.github_client import GitHubClient
from app.connectors.github.models import (
    GitHubCommit,
    GitHubIssue,
    GitHubIssueState,
    GitHubPullRequest,
    GitHubPullRequestState,
    GitHubRepository,
    GitHubWorkflowRun,
)


class GitHubConnector:
    """
    Enterprise GitHub connector.

    Responsibilities
    ----------------
    • Repository operations
    • Issue management
    • Pull request management
    • Commit retrieval
    • Workflow operations
    • Search

    The connector exposes domain models rather than raw GitHub
    REST API responses.
    """

    def __init__(
        self,
        client: GitHubClient,
    ) -> None:
        self._client = client

    # ==========================================================
    # Repository Operations
    # ==========================================================

    async def get_repository(
        self,
        owner: str,
        repository: str,
    ) -> GitHubRepository:
        """
        Retrieve repository metadata.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}"
        )

        return self._to_repository(response)

    async def list_repositories(
        self,
        organization: str,
        *,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubRepository]:
        """
        List repositories within an organization.
        """

        response = await self._client.get(
            f"/orgs/{organization}/repos",
            params={
                "page": page,
                "per_page": per_page,
            },
        )

        return [
            self._to_repository(item)
            for item in response
        ]

    async def repository_exists(
        self,
        owner: str,
        repository: str,
    ) -> bool:
        """
        Check if a repository exists.
        """

        try:
            await self.get_repository(
                owner,
                repository,
            )
            return True

        except Exception:
            return False

    # ==========================================================
    # Mapping
    # ==========================================================

    @staticmethod
    def _to_repository(
        payload: dict[str, Any],
    ) -> GitHubRepository:
        """
        Convert GitHub REST payload into a GitHubRepository.
        """

        owner = payload.get("owner") or {}

        return GitHubRepository(
            id=payload["id"],
            name=payload["name"],
            full_name=payload["full_name"],
            owner=owner.get("login", ""),
            private=payload["private"],
            default_branch=payload["default_branch"],
            description=payload.get("description"),
            clone_url=payload.get("clone_url"),
            html_url=payload.get("html_url"),
            language=payload.get("language"),
        )

    @staticmethod
    def _parse_datetime(
        value: str,
    ) -> datetime:
        """
        Parse GitHub datetime.
        """

        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        # ==========================================================
    # Issue Operations
    # ==========================================================

    async def list_issues(
        self,
        owner: str,
        repository: str,
        *,
        state: GitHubIssueState = GitHubIssueState.OPEN,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubIssue]:
        """
        List repository issues.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/issues",
            params={
                "state": state.value,
                "page": page,
                "per_page": per_page,
            },
        )

        issues: list[GitHubIssue] = []

        for item in response:
            # GitHub returns pull requests from this endpoint.
            if "pull_request" in item:
                continue

            issues.append(
                self._to_issue(
                    repository=f"{owner}/{repository}",
                    payload=item,
                )
            )

        return issues

    async def get_issue(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> GitHubIssue:
        """
        Retrieve a single issue.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/issues/{issue_number}"
        )

        return self._to_issue(
            repository=f"{owner}/{repository}",
            payload=response,
        )

    async def create_issue(
        self,
        owner: str,
        repository: str,
        *,
        title: str,
        body: str | None = None,
        labels: list[str] | None = None,
        assignee: str | None = None,
    ) -> GitHubIssue:
        """
        Create a GitHub issue.
        """

        payload: dict[str, Any] = {
            "title": title,
        }

        if body:
            payload["body"] = body

        if labels:
            payload["labels"] = labels

        if assignee:
            payload["assignees"] = [assignee]

        response = await self._client.post(
            f"/repos/{owner}/{repository}/issues",
            json=payload,
        )

        return self._to_issue(
            repository=f"{owner}/{repository}",
            payload=response,
        )

    async def update_issue(
        self,
        owner: str,
        repository: str,
        issue_number: int,
        *,
        title: str | None = None,
        body: str | None = None,
        labels: list[str] | None = None,
        assignee: str | None = None,
        state: GitHubIssueState | None = None,
    ) -> GitHubIssue:
        """
        Update an existing issue.
        """

        payload: dict[str, Any] = {}

        if title is not None:
            payload["title"] = title

        if body is not None:
            payload["body"] = body

        if labels is not None:
            payload["labels"] = labels

        if assignee is not None:
            payload["assignees"] = [assignee]

        if state is not None:
            payload["state"] = state.value

        response = await self._client.patch(
            f"/repos/{owner}/{repository}/issues/{issue_number}",
            json=payload,
        )

        return self._to_issue(
            repository=f"{owner}/{repository}",
            payload=response,
        )

    async def close_issue(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> GitHubIssue:
        """
        Close an issue.
        """

        return await self.update_issue(
            owner,
            repository,
            issue_number,
            state=GitHubIssueState.CLOSED,
        )

    # ==========================================================
    # Mapping
    # ==========================================================

    def _to_issue(
        self,
        *,
        repository: str,
        payload: dict[str, Any],
    ) -> GitHubIssue:
        """
        Convert a GitHub issue payload into a domain model.
        """

        assignee = payload.get("assignee")

        return GitHubIssue(
            id=payload["id"],
            number=payload["number"],
            title=payload["title"],
            state=GitHubIssueState(payload["state"]),
            repository=repository,
            author=payload["user"]["login"],
            created_at=self._parse_datetime(
                payload["created_at"]
            ),
            updated_at=self._parse_datetime(
                payload["updated_at"]
            ),
            body=payload.get("body"),
            assignee=(
                assignee["login"]
                if assignee
                else None
            ),
            labels=[
                label["name"]
                for label in payload.get("labels", [])
            ],
            metadata=payload.copy(),
        )
    
        # ==========================================================
    # Pull Request Operations
    # ==========================================================

    async def list_pull_requests(
        self,
        owner: str,
        repository: str,
        *,
        state: GitHubPullRequestState = GitHubPullRequestState.OPEN,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubPullRequest]:
        """
        List repository pull requests.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/pulls",
            params={
                "state": state.value.lower(),
                "page": page,
                "per_page": per_page,
            },
        )

        return [
            self._to_pull_request(
                repository=f"{owner}/{repository}",
                payload=item,
            )
            for item in response
        ]

    async def get_pull_request(
        self,
        owner: str,
        repository: str,
        pull_request_number: int,
    ) -> GitHubPullRequest:
        """
        Retrieve a pull request.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/pulls/{pull_request_number}"
        )

        return self._to_pull_request(
            repository=f"{owner}/{repository}",
            payload=response,
        )

    async def create_pull_request(
        self,
        owner: str,
        repository: str,
        *,
        title: str,
        source_branch: str,
        target_branch: str,
        body: str | None = None,
        draft: bool = False,
    ) -> GitHubPullRequest:
        """
        Create a pull request.
        """

        payload = {
            "title": title,
            "head": source_branch,
            "base": target_branch,
            "draft": draft,
        }

        if body is not None:
            payload["body"] = body

        response = await self._client.post(
            f"/repos/{owner}/{repository}/pulls",
            json=payload,
        )

        return self._to_pull_request(
            repository=f"{owner}/{repository}",
            payload=response,
        )

    async def merge_pull_request(
        self,
        owner: str,
        repository: str,
        pull_request_number: int,
        *,
        commit_title: str | None = None,
        commit_message: str | None = None,
        merge_method: str = "merge",
    ) -> bool:
        """
        Merge a pull request.

        Returns
        -------
        True if the merge succeeded.
        """

        payload: dict[str, Any] = {
            "merge_method": merge_method,
        }

        if commit_title:
            payload["commit_title"] = commit_title

        if commit_message:
            payload["commit_message"] = commit_message

        response = await self._client.put(
            f"/repos/{owner}/{repository}/pulls/{pull_request_number}/merge",
            json=payload,
        )

        return bool(response.get("merged", False))

    async def close_pull_request(
        self,
        owner: str,
        repository: str,
        pull_request_number: int,
    ) -> GitHubPullRequest:
        """
        Close a pull request without merging.
        """

        response = await self._client.patch(
            f"/repos/{owner}/{repository}/pulls/{pull_request_number}",
            json={
                "state": "closed",
            },
        )

        return self._to_pull_request(
            repository=f"{owner}/{repository}",
            payload=response,
        )

    # ==========================================================
    # Mapping
    # ==========================================================

    def _to_pull_request(
        self,
        *,
        repository: str,
        payload: dict[str, Any],
    ) -> GitHubPullRequest:
        """
        Convert a GitHub pull request payload into a domain model.
        """

        requested_reviewers = payload.get(
            "requested_reviewers",
            [],
        )

        return GitHubPullRequest(
            id=payload["id"],
            number=payload["number"],
            repository=repository,
            title=payload["title"],
            state=GitHubPullRequestState(
                payload["state"]
            ),
            author=payload["user"]["login"],
            source_branch=payload["head"]["ref"],
            target_branch=payload["base"]["ref"],
            created_at=self._parse_datetime(
                payload["created_at"]
            ),
            updated_at=self._parse_datetime(
                payload["updated_at"]
            ),
            merged=payload.get("merged", False),
            mergeable=payload.get("mergeable"),
            reviewers=[
                reviewer["login"]
                for reviewer in requested_reviewers
            ],
            metadata=payload.copy(),
        )
        
        # ==========================================================
    # Commit Operations
    # ==========================================================

    async def list_commits(
        self,
        owner: str,
        repository: str,
        *,
        branch: str | None = None,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubCommit]:
        """
        List commits for a repository.
        """

        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        if branch is not None:
            params["sha"] = branch

        response = await self._client.get(
            f"/repos/{owner}/{repository}/commits",
            params=params,
        )

        return [
            self._to_commit(item)
            for item in response
        ]

    async def get_commit(
        self,
        owner: str,
        repository: str,
        sha: str,
    ) -> GitHubCommit:
        """
        Retrieve a commit.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/commits/{sha}"
        )

        return self._to_commit(response)

    # ==========================================================
    # Workflow Operations
    # ==========================================================

    async def list_workflows(
        self,
        owner: str,
        repository: str,
    ) -> list[dict[str, Any]]:
        """
        List GitHub Actions workflows.

        Returns the raw workflow definitions. Workflow execution
        history is represented by GitHubWorkflowRun.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/actions/workflows"
        )

        return response.get("workflows", [])

    async def list_workflow_runs(
        self,
        owner: str,
        repository: str,
        *,
        workflow_id: int | None = None,
        branch: str | None = None,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubWorkflowRun]:
        """
        List workflow runs.
        """

        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }

        if branch:
            params["branch"] = branch

        if workflow_id is None:
            url = (
                f"/repos/{owner}/{repository}"
                "/actions/runs"
            )
        else:
            url = (
                f"/repos/{owner}/{repository}"
                f"/actions/workflows/{workflow_id}/runs"
            )

        response = await self._client.get(
            url,
            params=params,
        )

        return [
            self._to_workflow_run(item)
            for item in response.get("workflow_runs", [])
        ]

    async def trigger_workflow(
        self,
        owner: str,
        repository: str,
        workflow_id: str,
        *,
        ref: str,
        inputs: dict[str, Any] | None = None,
    ) -> None:
        """
        Trigger a GitHub Actions workflow_dispatch event.
        """

        payload: dict[str, Any] = {
            "ref": ref,
        }

        if inputs:
            payload["inputs"] = inputs

        await self._client.post(
            f"/repos/{owner}/{repository}"
            f"/actions/workflows/{workflow_id}/dispatches",
            json=payload,
        )

    # ==========================================================
    # Mapping
    # ==========================================================

    def _to_commit(
        self,
        payload: dict[str, Any],
    ) -> GitHubCommit:
        """
        Convert a GitHub commit payload.
        """

        commit = payload["commit"]

        author = commit.get("author") or {}

        return GitHubCommit(
            sha=payload["sha"],
            message=commit["message"],
            author=author.get("name", ""),
            timestamp=self._parse_datetime(
                author["date"]
            ),
            url=payload.get("html_url"),
        )

    def _to_workflow_run(
        self,
        payload: dict[str, Any],
    ) -> GitHubWorkflowRun:
        """
        Convert a GitHub workflow run payload.
        """

        return GitHubWorkflowRun(
            id=payload["id"],
            name=payload["name"],
            status=payload["status"],
            conclusion=payload.get("conclusion"),
            branch=payload["head_branch"],
            commit_sha=payload["head_sha"],
            created_at=self._parse_datetime(
                payload["created_at"]
            ),
            updated_at=self._parse_datetime(
                payload["updated_at"]
            ),
            html_url=payload.get("html_url"),
        )
        
        # ==========================================================
    # Repository Utilities
    # ==========================================================

    async def get_default_branch(
        self,
        owner: str,
        repository: str,
    ) -> str:
        """
        Returns the repository default branch.
        """

        repo = await self.get_repository(
            owner,
            repository,
        )

        return repo.default_branch

    async def list_branches(
        self,
        owner: str,
        repository: str,
        *,
        page: int = 1,
        per_page: int = 100,
    ) -> list[str]:
        """
        Returns repository branch names.
        """

        response = await self._client.get(
            f"/repos/{owner}/{repository}/branches",
            params={
                "page": page,
                "per_page": per_page,
            },
        )

        return [
            branch["name"]
            for branch in response
        ]

    async def branch_exists(
        self,
        owner: str,
        repository: str,
        branch: str,
    ) -> bool:
        """
        Returns True if the branch exists.
        """

        try:
            await self._client.get(
                f"/repos/{owner}/{repository}/branches/{branch}"
            )
            return True

        except Exception:
            return False

    # ==========================================================
    # Search
    # ==========================================================

    async def search_repositories(
        self,
        query: str,
        *,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubRepository]:
        """
        Search GitHub repositories.
        """

        response = await self._client.get(
            "/search/repositories",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
            },
        )

        return [
            self._to_repository(item)
            for item in response.get("items", [])
        ]

    async def search_issues(
        self,
        query: str,
        *,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubIssue]:
        """
        Search GitHub issues.
        """

        response = await self._client.get(
            "/search/issues",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
            },
        )

        issues: list[GitHubIssue] = []

        for item in response.get("items", []):

            repository_url = item.get(
                "repository_url",
                "",
            )

            repository = repository_url.split(
                "/repos/"
            )[-1]

            issues.append(
                self._to_issue(
                    repository=repository,
                    payload=item,
                )
            )

        return issues

    async def search_pull_requests(
        self,
        query: str,
        *,
        page: int = 1,
        per_page: int = 100,
    ) -> list[GitHubPullRequest]:
        """
        Search GitHub pull requests.

        GitHub exposes pull requests through the Search Issues API.
        The supplied query should include 'is:pr' when appropriate.
        """

        response = await self._client.get(
            "/search/issues",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
            },
        )

        pull_requests: list[GitHubPullRequest] = []

        for item in response.get("items", []):

            if "pull_request" not in item:
                continue

            owner = item["repository_url"].split("/")[-2]
            repository = item["repository_url"].split("/")[-1]

            pull_request = await self.get_pull_request(
                owner=owner,
                repository=repository,
                pull_request_number=item["number"],
            )

            pull_requests.append(
                pull_request
            )

        return pull_requests

    async def search_code(
        self,
        query: str,
        *,
        page: int = 1,
        per_page: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Search source code.

        Returns the GitHub search response directly because
        code search results do not map cleanly to a single
        domain model.
        """

        response = await self._client.get(
            "/search/code",
            params={
                "q": query,
                "page": page,
                "per_page": per_page,
            },
        )

        return response.get(
            "items",
            [],
        )

    # ==========================================================
    # Lifecycle
    # ==========================================================

    async def close(
        self,
    ) -> None:
        """
        Release HTTP resources.
        """

        await self._client.close()
        
        # ==========================================================
    # Repository Analysis
    # ==========================================================

    async def analyze_repository(
        self,
        owner: str,
        repository: str,
    ) -> dict[str, Any]:
        """
        Perform a high-level analysis of a repository.

        The analysis aggregates existing repository information using
        connector operations without introducing additional GitHub API
        integrations.

        Returns
        -------
        Dictionary containing repository metadata and activity metrics.
        """

        repo = await self.get_repository(
            owner=owner,
            repository=repository,
        )

        issues = await self.list_issues(
            owner=owner,
            repository=repository,
        )

        pull_requests = await self.list_pull_requests(
            owner=owner,
            repository=repository,
        )

        branches = await self.list_branches(
            owner=owner,
            repository=repository,
        )

        workflow_runs = await self.list_workflow_runs(
            owner=owner,
            repository=repository,
        )

        return {
            "repository": repo,
            "summary": {
                "branches": len(branches),
                "open_issues": len(issues),
                "open_pull_requests": len(pull_requests),
                "workflow_runs": len(workflow_runs),
                "default_branch": repo.default_branch,
                "language": repo.language,
            },
        }
        
        
    async def repository_health(
        self,
        owner: str,
        repository: str,
    ) -> dict[str, Any]:
        """
        Produce a lightweight repository health report.

        The report is intentionally derived from existing connector
        capabilities without performing static code analysis.
        """

        analysis = await self.analyze_repository(
            owner=owner,
            repository=repository,
        )

        summary = analysis["summary"]

        score = 100

        score -= min(summary["open_issues"], 20)

        score -= min(summary["open_pull_requests"], 20)

        if summary["workflow_runs"] == 0:
            score -= 10

        score = max(score, 0)

        return {
            "score": score,
            "healthy": score >= 80,
            "summary": summary,
            "recommendations": [
                recommendation
                for recommendation in (
                    "Reduce open pull requests."
                    if summary["open_pull_requests"] > 10
                    else None,
                    "Review repository issues."
                    if summary["open_issues"] > 20
                    else None,
                    "Configure GitHub Actions."
                    if summary["workflow_runs"] == 0
                    else None,
                )
                if recommendation
            ],
        }
    
    async def code_quality(
        self,
        owner: str,
        repository: str,
    ) -> dict[str, Any]:
        """
        Produce a lightweight code quality assessment.

        This assessment is heuristic-based and relies only on existing
        repository metadata exposed through the connector.
        """

        analysis = await self.analyze_repository(
            owner=owner,
            repository=repository,
        )

        summary = analysis["summary"]

        score = 100.0

        score -= min(summary["open_issues"] * 0.5, 15)

        score -= min(summary["open_pull_requests"] * 0.75, 15)

        if summary["workflow_runs"] == 0:
            score -= 10

        score = round(max(score, 0), 2)

        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[str] = []

        if summary["workflow_runs"] > 0:
            strengths.append("GitHub Actions workflows are configured.")
        else:
            weaknesses.append("No GitHub Actions workflows detected.")
            recommendations.append(
                "Introduce CI validation using GitHub Actions."
            )

        if summary["open_pull_requests"] <= 5:
            strengths.append("Pull request backlog is under control.")
        else:
            weaknesses.append("Large pull request backlog.")
            recommendations.append(
                "Review and merge stale pull requests."
            )

        if summary["open_issues"] <= 10:
            strengths.append("Issue backlog is manageable.")
        else:
            weaknesses.append("High number of open issues.")
            recommendations.append(
                "Reduce outstanding GitHub issues."
            )

        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }
    
    async def review_pull_request(
        self,
        owner: str,
        repository: str,
        pull_request_number: int,
    ) -> dict[str, Any]:
        """
        Retrieve pull request information and generate a review summary.

        This method intentionally performs repository analysis only.
        It does not submit a GitHub review.
        """

        pull_request = await self.get_pull_request(
            owner=owner,
            repository=repository,
            pull_request_number=pull_request_number,
        )

        recommendations: list[str] = []

        if not pull_request.mergeable:
            recommendations.append(
                "Resolve merge conflicts before merging."
            )

        if not pull_request.reviewers:
            recommendations.append(
                "Assign reviewers before approval."
            )

        if not recommendations:
            recommendations.append(
                "Pull request appears ready for review."
            )

        return {
            "pull_request": pull_request,
            "mergeable": pull_request.mergeable,
            "merged": pull_request.merged,
            "reviewers": pull_request.reviewers,
            "recommendations": recommendations,
        }