"""
Enterprise DevOps Agent.

Business orchestration layer responsible for DevOps capabilities.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from app.agents.devops.devops_actions import DevOpsActions
from app.agents.devops.exceptions import (
    UnsupportedCapabilityError,
)
from app.agents.devops.models import (
    DevOpsAgentRequest,
    DevOpsAgentResponse,
    DevOpsCapability,
    DevOpsExecutionMetadata,
)

logger = logging.getLogger(__name__)

AsyncHandler = Callable[
    [DevOpsAgentRequest],
    Awaitable[Any],
]


class DevOpsAgent:
    """
    Enterprise DevOps Agent.

    This class performs orchestration only.
    """

    def __init__(
        self,
        devops_actions: DevOpsActions,
    ) -> None:

        self._actions = devops_actions

        self._handlers: dict[
            DevOpsCapability,
            AsyncHandler,
        ] = {

            #
            # Repository
            #

            DevOpsCapability.REPOSITORY_ANALYSIS:
                self._actions.repository_analysis,

            DevOpsCapability.REPOSITORY_HEALTH:
                self._actions.repository_health,

            DevOpsCapability.CODE_QUALITY:
                self._actions.code_quality,

            #
            # Pull Requests
            #

            DevOpsCapability.PULL_REQUEST_REVIEW:
                self._actions.pull_request_review,

            #
            # DevOps
            #

            DevOpsCapability.RELEASE_READINESS:
                self._actions.release_readiness,

            DevOpsCapability.INCIDENT_ANALYSIS:
                self._actions.incident_analysis,

            DevOpsCapability.GENERATE_RELEASE_NOTES:
                self._actions.generate_release_notes,

            DevOpsCapability.GENERATE_RUNBOOK:
                self._actions.generate_runbook,

            DevOpsCapability.SUMMARIZE_DEPLOYMENT:
                self._actions.summarize_deployment,
        }

    # ==========================================================
    # Public API
    # ==========================================================

    async def execute(
        self,
        request: DevOpsAgentRequest,
    ) -> DevOpsAgentResponse:

        logger.info(
            "Executing DevOps capability '%s'.",
            request.capability.value,
        )

        metadata = DevOpsExecutionMetadata()

        await self._authorize(
            metadata,
        )

        try:

            handler = self._handlers.get(
                request.capability,
            )

            if handler is None:

                raise UnsupportedCapabilityError(
                    request.capability.value,
                )

            result = await handler(
                request,
            )

            return DevOpsAgentResponse(
                success=True,
                capability=request.capability,
                message="Capability executed successfully.",
                result=result,
                metadata=metadata,
            )

        except Exception as exc:

            logger.exception(
                "DevOps execution failed."
            )

            return DevOpsAgentResponse(
                success=False,
                capability=request.capability,
                message=str(exc),
                result=None,
                metadata=metadata,
            )
    
        # ==========================================================
    # Governance
    # ==========================================================

    async def _authorize(
        self,
        metadata: DevOpsExecutionMetadata,
    ) -> None:
        """
        Governance authorization.

        Future integration point for Governance Runtime.
        """

        metadata.governance_approved = True

    # ==========================================================
    # Capability Discovery
    # ==========================================================

    @property
    def supported_capabilities(
        self,
    ) -> tuple[DevOpsCapability, ...]:
        """
        Return supported capabilities.
        """

        return tuple(
            self._handlers.keys()
        )

    def supports(
        self,
        capability: DevOpsCapability | str,
    ) -> bool:
        """
        Determine whether this agent supports
        the requested capability.
        """

        if isinstance(
            capability,
            str,
        ):
            try:
                capability = DevOpsCapability(
                    capability,
                )
            except ValueError:
                return False

        return capability in self._handlers

    # ==========================================================
    # Information
    # ==========================================================

    @property
    def name(
        self,
    ) -> str:
        """
        Agent name.
        """

        return "devops"

    @property
    def description(
        self,
    ) -> str:
        """
        Agent description.
        """

        return (
            "Enterprise DevOps Agent responsible "
            "for repository health, release readiness, "
            "incident analysis and operational insights."
        )

    def capabilities(
        self,
    ) -> list[str]:
        """
        Return supported capability names.
        """

        return [
            capability.value
            for capability in self.supported_capabilities
        ]

    def __repr__(
        self,
    ) -> str:
        """
        Debug representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(capabilities={len(self._handlers)})"
        )
        
    