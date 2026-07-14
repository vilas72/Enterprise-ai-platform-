"""
Jira business actions for the Developer Agent.

This module encapsulates Jira-related business capabilities exposed by
the Developer Agent. It translates business requests into Jira
operations using the Enterprise JiraConnector.

No REST API logic should exist in this layer.
"""

from __future__ import annotations

import logging

from app.agents.developer.models import (
    DeveloperAgentRequest,
    JiraIssueReference,
)
from app.connectors.jira.jira_connector import JiraConnector
from app.connectors.jira.models import (
    JiraIssue,
    JiraIssueType,
)

logger = logging.getLogger(__name__)


class JiraActions:
    """
    Enterprise Jira business actions.

    Responsibilities
    ----------------

    • Create Bug
    • Create Story
    • Transition Issue

    This class contains business orchestration only.
    """

    def __init__(
        self,
        jira_connector: JiraConnector,
    ) -> None:
        self._jira = jira_connector

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _require_project_key(
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Validate project key.
        """

        project_key = request.metadata.get("project_key")

        if not project_key:
            raise ValueError(
                "project_key is required."
            )

        return project_key

    @staticmethod
    def _require_issue(
        request: DeveloperAgentRequest,
    ) -> JiraIssueReference:
        """
        Validate Jira issue.
        """

        if request.jira_issue is None:
            raise ValueError(
                "Jira issue is required."
            )

        return request.jira_issue

    @staticmethod
    def _require_transition(
        request: DeveloperAgentRequest,
    ) -> str:
        """
        Validate transition id.
        """

        transition_id = request.metadata.get(
            "transition_id"
        )

        if not transition_id:
            raise ValueError(
                "transition_id is required."
            )

        return transition_id

    # ------------------------------------------------------------------
    # Issue Creation
    # ------------------------------------------------------------------

    async def create_bug(
        self,
        request: DeveloperAgentRequest,
    ) -> JiraIssue:
        """
        Create a Jira Bug.
        """

        project_key = self._require_project_key(
            request
        )

        if not request.title:
            raise ValueError(
                "Issue title is required."
            )

        logger.info(
            "Creating Jira Bug in project %s",
            project_key,
        )

        return await self._jira.create_issue(
            project_key=project_key,
            summary=request.title,
            description=request.description,
            issue_type=JiraIssueType.BUG,
        )

    async def create_story(
        self,
        request: DeveloperAgentRequest,
    ) -> JiraIssue:
        """
        Create a Jira Story.
        """

        project_key = self._require_project_key(
            request
        )

        if not request.title:
            raise ValueError(
                "Issue title is required."
            )

        logger.info(
            "Creating Jira Story in project %s",
            project_key,
        )

        return await self._jira.create_issue(
            project_key=project_key,
            summary=request.title,
            description=request.description,
            issue_type=JiraIssueType.STORY,
        )
        
        # ------------------------------------------------------------------
    # Issue Transition
    # ------------------------------------------------------------------

    async def transition_issue(
        self,
        request: DeveloperAgentRequest,
    ) -> JiraIssue:
        """
        Transition an existing Jira issue.
        """

        issue = self._require_issue(request)

        transition_id = self._require_transition(
            request
        )

        logger.info(
            "Transitioning Jira issue %s using transition %s",
            issue.issue_key,
            transition_id,
        )

        return await self._jira.transition_issue(
            issue_key=issue.issue_key,
            transition_id=transition_id,
        )

    # ------------------------------------------------------------------
    # Generic Dispatcher
    # ------------------------------------------------------------------

    async def execute(
        self,
        capability: str,
        request: DeveloperAgentRequest,
    ) -> JiraIssue:
        """
        Execute a Jira capability.

        This provides a single entry point for the DeveloperAgent while
        keeping all Jira-specific business logic encapsulated in this
        class.
        """

        handlers = {
            "create_jira_bug": self.create_bug,
            "create_jira_story": self.create_story,
            "transition_jira_issue": self.transition_issue,
        }

        handler = handlers.get(capability)

        if handler is None:
            raise ValueError(
                f"Unsupported Jira capability: {capability}"
            )

        return await handler(request)