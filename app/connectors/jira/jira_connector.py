from __future__ import annotations

from datetime import datetime
from typing import Any

from app.connectors.jira.jira_client import JiraClient
from app.connectors.jira.models import (
    JiraComment,
    JiraIssue,
    JiraIssueStatus,
    JiraIssueType,
    JiraPriority,
    JiraProject,
    JiraSprint,
)


class JiraConnector:
    """
    Enterprise Jira connector.

    Responsibilities
    ----------------
    • Project operations
    • Issue management
    • Sprint management
    • Comment management
    • Search

    The connector returns strongly typed domain models
    instead of raw Jira REST payloads.
    """

    def __init__(
        self,
        client: JiraClient,
    ) -> None:
        self._client = client

    # ==========================================================
    # Project Operations
    # ==========================================================

    async def get_project(
        self,
        project_key: str,
    ) -> JiraProject:
        """
        Retrieve project information.
        """

        response = await self._client.get(
            f"/rest/api/3/project/{project_key}"
        )

        return self._to_project(response)

    async def list_projects(
        self,
    ) -> list[JiraProject]:
        """
        Returns all accessible projects.
        """

        response = await self._client.get(
            "/rest/api/3/project/search"
        )

        return [
            self._to_project(item)
            for item in response.get(
                "values",
                [],
            )
        ]

    async def project_exists(
        self,
        project_key: str,
    ) -> bool:
        """
        Returns True if a project exists.
        """

        try:
            await self.get_project(
                project_key,
            )
            return True

        except Exception:
            return False

    # ==========================================================
    # Mapping
    # ==========================================================

    @staticmethod
    def _to_project(
        payload: dict[str, Any],
    ) -> JiraProject:
        """
        Convert Jira project payload.
        """

        return JiraProject(
            id=payload["id"],
            key=payload["key"],
            name=payload["name"],
            project_type=payload.get(
                "projectTypeKey",
                "",
            ),
            url=payload.get("self"),
            metadata=payload.copy(),
        )

    @staticmethod
    def _parse_datetime(
        value: str,
    ) -> datetime:
        """
        Parse Jira timestamps.
        """

        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        
        # ==========================================================
    # Issue Operations
    # ==========================================================

    async def get_issue(
        self,
        issue_key: str,
    ) -> JiraIssue:
        """
        Retrieve a Jira issue.
        """

        response = await self._client.get(
            f"/rest/api/3/issue/{issue_key}"
        )

        return self._to_issue(response)

    async def search_issues(
        self,
        jql: str,
        *,
        start_at: int = 0,
        max_results: int = 100,
    ) -> list[JiraIssue]:
        """
        Search issues using JQL.
        """

        response = await self._client.post(
            "/rest/api/3/search",
            json={
                "jql": jql,
                "startAt": start_at,
                "maxResults": max_results,
            },
        )

        return [
            self._to_issue(issue)
            for issue in response.get("issues", [])
        ]

    async def create_issue(
        self,
        *,
        project_key: str,
        summary: str,
        issue_type: JiraIssueType,
        description: str | None = None,
        priority: JiraPriority | None = None,
        labels: list[str] | None = None,
        assignee: str | None = None,
    ) -> JiraIssue:
        """
        Create a Jira issue.
        """

        fields: dict[str, Any] = {
            "project": {
                "key": project_key,
            },
            "summary": summary,
            "issuetype": {
                "name": issue_type.value,
            },
        }

        if description:
            fields["description"] = self._to_adf(description)

        if priority:
            fields["priority"] = {
                "name": priority.value,
            }

        if labels:
            fields["labels"] = labels

        if assignee:
            fields["assignee"] = {
                "accountId": assignee,
            }

        response = await self._client.post(
            "/rest/api/3/issue",
            json={
                "fields": fields,
            },
        )

        return await self.get_issue(
            response["key"]
        )

    async def update_issue(
        self,
        issue_key: str,
        *,
        summary: str | None = None,
        description: str | None = None,
        priority: JiraPriority | None = None,
        labels: list[str] | None = None,
    ) -> JiraIssue:
        """
        Update a Jira issue.
        """

        fields: dict[str, Any] = {}

        if summary is not None:
            fields["summary"] = summary

        if description is not None:
            fields["description"] = self._to_adf(description)

        if priority is not None:
            fields["priority"] = {
                "name": priority.value,
            }

        if labels is not None:
            fields["labels"] = labels

        await self._client.put(
            f"/rest/api/3/issue/{issue_key}",
            json={
                "fields": fields,
            },
        )

        return await self.get_issue(
            issue_key
        )

    async def transition_issue(
        self,
        issue_key: str,
        transition_id: str,
    ) -> JiraIssue:
        """
        Transition a Jira issue to another workflow state.
        """

        await self._client.post(
            f"/rest/api/3/issue/{issue_key}/transitions",
            json={
                "transition": {
                    "id": transition_id,
                }
            },
        )

        return await self.get_issue(
            issue_key
        )

    # ==========================================================
    # Mapping
    # ==========================================================

    def _to_issue(
        self,
        payload: dict[str, Any],
    ) -> JiraIssue:
        """
        Convert a Jira issue payload into a domain model.
        """

        fields = payload["fields"]

        assignee = fields.get("assignee")
        reporter = fields.get("reporter")
        priority = fields.get("priority")

        status_name = (
            fields.get("status", {})
            .get("name", "To Do")
        )

        try:
            status = JiraIssueStatus(status_name)
        except ValueError:
            status = JiraIssueStatus.TO_DO

        issue_type_name = (
            fields["issuetype"]["name"]
        )

        try:
            issue_type = JiraIssueType(
                issue_type_name
            )
        except ValueError:
            issue_type = JiraIssueType.TASK

        priority_value = None

        if priority:
            try:
                priority_value = JiraPriority(
                    priority["name"]
                )
            except ValueError:
                priority_value = None

        return JiraIssue(
            id=payload["id"],
            key=payload["key"],
            project_key=fields["project"]["key"],
            summary=fields["summary"],
            description=self._from_adf(fields.get("description")),
            issue_type=issue_type,
            status=status,
            priority=priority_value,
            assignee=(
                assignee["displayName"]
                if assignee
                else None
            ),
            reporter=(
                reporter["displayName"]
                if reporter
                else None
            ),
            created_at=self._parse_datetime(
                fields["created"]
            ),
            updated_at=self._parse_datetime(
                fields["updated"]
            ),
            labels=fields.get(
                "labels",
                [],
            ),
            metadata=payload.copy(),
        )
    
        # ==========================================================
    # Comment Operations
    # ==========================================================

    async def list_comments(
        self,
        issue_key: str,
    ) -> list[JiraComment]:
        """
        Returns all comments for an issue.
        """

        response = await self._client.get(
            f"/rest/api/3/issue/{issue_key}/comment"
        )

        return [
            self._to_comment(comment)
            for comment in response.get(
                "comments",
                [],
            )
        ]

    async def add_comment(
        self,
        issue_key: str,
        body: str,
    ) -> JiraComment:
        """
        Add a comment to an issue.
        """

        response = await self._client.post(
            f"/rest/api/3/issue/{issue_key}/comment",
            json={
                "body": body,
            },
        )

        return self._to_comment(response)

    async def delete_comment(
        self,
        issue_key: str,
        comment_id: str,
    ) -> None:
        """
        Delete an issue comment.
        """

        await self._client.delete(
            f"/rest/api/3/issue/{issue_key}/comment/{comment_id}"
        )

    # ==========================================================
    # Assignment
    # ==========================================================

    async def assign_issue(
        self,
        issue_key: str,
        account_id: str,
    ) -> JiraIssue:
        """
        Assign an issue.
        """

        await self._client.put(
            f"/rest/api/3/issue/{issue_key}/assignee",
            json={
                "accountId": account_id,
            },
        )

        return await self.get_issue(
            issue_key
        )

    # ==========================================================
    # Sprint Operations
    # ==========================================================

    async def list_sprints(
        self,
        board_id: int,
    ) -> list[JiraSprint]:
        """
        Returns board sprints.
        """

        response = await self._client.get(
            f"/rest/agile/1.0/board/{board_id}/sprint"
        )

        return [
            self._to_sprint(item)
            for item in response.get(
                "values",
                [],
            )
        ]

    async def get_sprint(
        self,
        sprint_id: int,
    ) -> JiraSprint:
        """
        Retrieve sprint information.
        """

        response = await self._client.get(
            f"/rest/agile/1.0/sprint/{sprint_id}"
        )

        return self._to_sprint(
            response,
        )

    # ==========================================================
    # Mapping
    # ==========================================================

    def _to_comment(
        self,
        payload: dict[str, Any],
    ) -> JiraComment:
        """
        Convert Jira comment.
        """

        author = payload.get(
            "author",
            {},
        )

        return JiraComment(
            id=payload["id"],
            author=author.get(
                "displayName",
                "",
            ),
            body=self._from_adf(
                payload.get("body")
            ),
            created_at=self._parse_datetime(
                payload["created"]
            ),
            updated_at=self._parse_datetime(
                payload["updated"]
            ),
            metadata=payload.copy(),
        )

    def _to_sprint(
        self,
        payload: dict[str, Any],
    ) -> JiraSprint:
        """
        Convert Jira sprint.
        """

        start_date = payload.get(
            "startDate",
        )

        end_date = payload.get(
            "endDate",
        )

        return JiraSprint(
            id=payload["id"],
            name=payload["name"],
            state=payload["state"],
            start_date=(
                self._parse_datetime(start_date)
                if start_date
                else None
            ),
            end_date=(
                self._parse_datetime(end_date)
                if end_date
                else None
            ),
            goal=payload.get(
                "goal",
            ),
            metadata=payload.copy(),
        )
        
        # ==========================================================
    # Issue Maintenance
    # ==========================================================

    async def delete_issue(
        self,
        issue_key: str,
        *,
        delete_subtasks: bool = False,
    ) -> None:
        """
        Delete a Jira issue.
        """

        await self._client.delete(
            f"/rest/api/3/issue/{issue_key}"
            f"?deleteSubtasks={str(delete_subtasks).lower()}"
        )

    # ==========================================================
    # Project Utilities
    # ==========================================================

    async def issue_exists(
        self,
        issue_key: str,
    ) -> bool:
        """
        Returns True if the issue exists.
        """

        try:
            await self.get_issue(issue_key)
            return True
        except Exception:
            return False

    async def get_project_issue_count(
        self,
        project_key: str,
    ) -> int:
        """
        Returns the number of issues in a project.
        """

        response = await self._client.post(
            "/rest/api/3/search",
            json={
                "jql": f"project={project_key}",
                "maxResults": 0,
            },
        )

        return response.get("total", 0)

    # ==========================================================
    # Atlassian Document Format (ADF)
    # ==========================================================

    @staticmethod
    def _to_adf(
        text: str,
    ) -> dict[str, Any]:
        """
        Convert plain text into Atlassian Document Format.
        """

        return {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                        }
                    ],
                }
            ],
        }

    @staticmethod
    def _from_adf(
        document: Any,
    ) -> str:
        """
        Convert Atlassian Document Format into plain text.

        The conversion intentionally extracts text only.
        """

        if not isinstance(document, dict):
            return ""

        content = document.get(
            "content",
            [],
        )

        lines: list[str] = []

        for block in content:

            for item in block.get(
                "content",
                [],
            ):

                text = item.get("text")

                if text:
                    lines.append(text)

        return "\n".join(lines)

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