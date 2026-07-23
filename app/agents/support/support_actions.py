"""
Enterprise Support business actions.

This module orchestrates support workflows by coordinating
existing business actions. It intentionally contains no
connector, retrieval, or AI implementation logic.
"""

from __future__ import annotations

import logging

from app.actions.ai_actions import AIActions
from app.actions.jira_actions import JiraActions
from app.actions.knowledge_actions import KnowledgeActions
from app.agents.support.models import (
    SupportAgentRequest,
)

from app.actions.jira_actions import TicketSearchRequest

logger = logging.getLogger(__name__)


class SupportActions:
    """
    Enterprise Support business actions.

    Responsibilities
    ----------------
    - Ticket lifecycle orchestration
    - Knowledge recommendation
    - Incident assistance
    - Resolution generation
    - Escalation workflows

    Business implementations remain inside the existing
    JiraActions, KnowledgeActions and AIActions.
    """

    def __init__(
        self,
        jira_actions: JiraActions,
        knowledge_actions: KnowledgeActions,
        ai_actions: AIActions,
    ) -> None:

        self._jira = jira_actions
        self._knowledge = knowledge_actions
        self._ai = ai_actions

    # ------------------------------------------------------------------
    # Ticket Operations
    # ------------------------------------------------------------------

    async def search_tickets(
        self,
        request: SupportAgentRequest,
    ):

        search_request = TicketSearchRequest(
            query=request.query or "",
            project=request.project_key,
            status=request.status or [],
            assignee=request.assignee,
            max_results=request.max_results or 20,
        )
            
        logger.info("Jira returned %d issues", len(await self._jira.search_issues(search_request)))

        issues = await self._jira.search_issues(
            search_request,
        )

        logger.info(
            "Jira returned %d issues",
            len(issues),
        )

        return issues
        

    async def create_ticket(
        self,
        request: SupportAgentRequest,
    ):
        """
        Create a support ticket.
        """

        logger.debug("Creating support ticket.")

        return await self._jira.create_story(request)

    async def update_ticket(
        self,
        request: SupportAgentRequest,
    ):
        """
        Update a support ticket.
        """

        logger.debug("Updating support ticket.")

        return await self._jira.update_issue(
            issue_key=request.ticket_key,
            summary=request.title,
            description=request.description, 
        )

    async def transition_ticket(
        self,
        request: SupportAgentRequest,
    ):
        """
        Transition a support ticket.
        """

        logger.debug("Transitioning support ticket.")

        return await self._jira.transition_issue(request)

    # ------------------------------------------------------------------
    # Knowledge
    # ------------------------------------------------------------------

    async def search_knowledge(
        self,
        request: SupportAgentRequest,
    ):
        """
        Search enterprise knowledge.
        """

        logger.debug("Searching enterprise knowledge.")

        return await self._knowledge.search(request)

    async def recommend_articles(
        self,
        request: SupportAgentRequest,
    ):
        """
        Recommend knowledge articles.
        """

        logger.debug("Generating knowledge recommendations.")

        return await self._knowledge.recommend(request)

    async def similar_incidents(
        self,
        request: SupportAgentRequest,
    ):
        """
        Find similar incidents.
        """

        logger.debug("Searching similar incidents.")

        return await self._knowledge.answer(request)

    # ------------------------------------------------------------------
    # AI Assistance
    # ------------------------------------------------------------------

    async def summarize_incident(
        self,
        request: SupportAgentRequest,
    ):
        """
        Summarize incident details.
        """

        logger.debug("Summarizing incident.")

        return await self._ai.summarize(request.query or "")

    async def generate_resolution(
        self,
        request: SupportAgentRequest,
    ):
        """
        Generate a suggested resolution.
        """

        logger.debug("Generating resolution.")

        return await self._ai.generate_resolution(
            request
        )

    async def escalation_recommendation(
        self,
        request: SupportAgentRequest,
    ):
        """
        Generate escalation recommendation.
        """

        logger.debug("Generating escalation recommendation.")

        return await self._ai.escalation_recommendation(
            request.query or ""
        )
        
    