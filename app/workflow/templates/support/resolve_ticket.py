"""
Support Ticket Resolution Workflow Template.
"""

from __future__ import annotations
from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class ResolveTicketTemplate(WorkflowTemplate):
    """
    Workflow template for resolving enterprise support tickets.

    Workflow:

        Fetch Ticket
              ↓
        Collect Logs
              ↓
        Search Knowledge Base
              ↓
        Analyze Root Cause
              ↓
        Generate Resolution
              ↓
        Update Ticket
              ↓
        Notify User
    """

    def __init__(self) -> None:
        super().__init__(
            capability="resolve_ticket",
            name="Resolve Support Ticket",
            description="Analyze and resolve an enterprise support ticket.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                    id="search_tickets",
                    name="Fetch Ticket",
                    agent="support",
                    capability="search_tickets",
                    action=ActionType.FETCH_TICKET,
                ),
                WorkflowStep(
                    id="search_knowledge",
                    name="Search Knowledge Base",
                    agent="support",
                    capability="search_knowledge",
                    action=ActionType.SEARCH_KNOWLEDGE,
                    depends_on=["search_tickets"],
                ),
                #WorkflowStep(
                #    id="analyze_root_cause",
                #    name="Analyze Root Cause",
                #    agent="support",
                #    capability="analyze_root_cause",
                #    action=ActionType.ANALYZE_ROOT_CAUSE,
                #    depends_on=[
                #        "search_tickets",
                #        "search_knowledge",
                #    ],
                #),
                WorkflowStep(
                    id="generate_resolution",
                    name="Generate Resolution",
                    agent="support",
                    capability="generate_resolution",
                    action=ActionType.GENERATE_RESOLUTION,
                    depends_on=["search_knowledge"],
                ),
                WorkflowStep(
                    id="update_ticket",
                    name="Update Ticket",
                    agent="support",
                    capability="update_ticket",
                    action=ActionType.UPDATE_TICKET,
                    depends_on=["generate_resolution"],
                ),
                WorkflowStep(
                    id="notify_user",
                    name="Notify User",
                    agent="support",
                    capability="notify_user",
                    action=ActionType.NOTIFY_USER,
                    depends_on=["update_ticket"],
                ),
            ],
        )

