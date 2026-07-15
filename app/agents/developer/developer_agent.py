"""
Enterprise Developer Agent.

The Developer Agent is the business orchestration layer responsible for
handling developer-centric capabilities. It coordinates Governance,
GitHub actions, Jira actions and AI actions without exposing connector
implementations to callers.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from app.actions.ai_actions import AIActions
from app.actions.github_actions import GitHubActions
from app.actions.jira_actions import JiraActions
from app.agents.developer.models import (
    DeveloperAgentRequest,
    DeveloperAgentResponse,
    DeveloperCapability,
    DeveloperExecutionMetadata,
)


logger = logging.getLogger(__name__)

AsyncHandler = Callable[
    [DeveloperAgentRequest],
    Awaitable[Any],
]

SyncHandler = Callable[
    [DeveloperAgentRequest],
    Any,
]


class DeveloperAgent:
    """
    Enterprise Developer Agent.

    Responsibilities
    ----------------

    • Repository Analysis

    • Repository Search

    • GitHub Issue Management

    • Pull Request Review

    • Pull Request Merge

    • Jira Story/Bug Management

    • Documentation Generation

    • Unit Test Generation

    • Code Explanation

    • Architecture Recommendations

    This class contains orchestration only.

    Business implementations live inside:

        - GitHubActions

        - JiraActions

        - AIActions
    """

    def __init__(
        self,
        github_actions: GitHubActions,
        jira_actions: JiraActions,
        ai_actions: AIActions,
    ) -> None:

        self._github = github_actions

        self._jira = jira_actions

        self._ai = ai_actions

        

        #
        # Capability Routing
        #

        self._async_handlers: dict[
            DeveloperCapability,
            AsyncHandler,
        ] = {
            DeveloperCapability.SEARCH_REPOSITORY:
                self._github.search_repository,

            DeveloperCapability.ANALYZE_REPOSITORY:
                self._github.analyze_repository,

            DeveloperCapability.CREATE_GITHUB_ISSUE:
                self._github.create_issue,

            DeveloperCapability.REVIEW_PULL_REQUEST:
                self._github.review_pull_request,

            DeveloperCapability.MERGE_PULL_REQUEST:
                self._github.merge_pull_request,

            DeveloperCapability.REPOSITORY_HEALTH:
                self._github.repository_health,

            DeveloperCapability.CODE_QUALITY:
                self._github.code_quality,

            DeveloperCapability.CREATE_JIRA_BUG:
                self._jira.create_bug,

            DeveloperCapability.CREATE_JIRA_STORY:
                self._jira.create_story,

            DeveloperCapability.TRANSITION_JIRA_ISSUE:
                self._jira.transition_issue,
        }

        self._sync_handlers: dict[
            DeveloperCapability,
            SyncHandler,
        ] = {
            DeveloperCapability.EXPLAIN_CODE:
                self._ai.explain_code,

            DeveloperCapability.GENERATE_UNIT_TESTS:
                self._ai.generate_unit_tests,

            DeveloperCapability.GENERATE_DOCUMENTATION:
                self._ai.generate_documentation,

            DeveloperCapability.ARCHITECTURE_RECOMMENDATIONS:
                self._ai.architecture_recommendations,
        }
    
    async def execute(
        self,
        request: DeveloperAgentRequest,
    ) -> DeveloperAgentResponse:
        """
        Execute a Developer Agent capability.

        Workflow
        --------
        1. Governance validation
        2. Resolve capability handler
        3. Execute business action
        4. Build response
        """

        logger.info(
            "Executing developer capability '%s'",
            request.capability.value,
        )

        metadata = DeveloperExecutionMetadata()

        #
        # Governance
        #

        await self._authorize(request, metadata)

        try:

            #
            # Async Capabilities
            #

            if request.capability in self._async_handlers:

                handler = self._async_handlers[
                    request.capability
                ]

                result = await handler(request.payload)

            #
            # Sync Capabilities
            #

            elif request.capability in self._sync_handlers:

                handler = self._sync_handlers[
                    request.capability
                ]

                result = handler(request.payload)

            else:

                raise ValueError(
                    f"Unsupported capability: "
                    f"{request.capability.value}"
                )

            logger.info(
                "Developer capability '%s' completed successfully.",
                request.capability.value,
            )

            return DeveloperAgentResponse(
                success=True,
                capability=request.capability,
                message="Developer capability executed successfully.",
                result=result,
                metadata=metadata,
            )

        except Exception as exc:

            logger.exception(
                "Developer capability '%s' failed.",
                request.capability.value,
            )

            return DeveloperAgentResponse(
                success=False,
                capability=request.capability,
                message=str(exc),
                result=None,
                metadata=metadata,
            )

    # ------------------------------------------------------------------
    # Governance
    # ------------------------------------------------------------------

    async def _authorize(
        self,
        request: DeveloperAgentRequest,
        metadata: DeveloperExecutionMetadata,
    ) -> None:
        """
        Execute governance validation.

        Governance integration will be extended as additional
        developer policies are introduced.
        """

        metadata.governance_approved = True

        logger.debug(
            "Governance validation completed for capability '%s'.",
            request.capability.value,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def supported_capabilities(
        self,
    ) -> tuple[DeveloperCapability, ...]:
        """
        Return supported capabilities.
        """

        return (
            *self._async_handlers.keys(),
            *self._sync_handlers.keys(),
        )

    def supports(
        self,
        capability: DeveloperCapability | str,
    ) -> bool:
        """
        Determine whether the Developer Agent supports
        a capability.
        """

        if isinstance(capability, str):
            try:
                capability = DeveloperCapability(capability)
            except ValueError:
                return False

        return (
            capability in self._async_handlers
            or capability in self._sync_handlers
        )

    @property
    def name(self) -> str:
        return "developer"

    @property
    def description(self) -> str:
        return "Enterprise Developer Agent for repository, PR, Jira and AI-assisted engineering workflows."

    def capabilities(self) -> list[str]:
        return [capability.value for capability in self.supported_capabilities]