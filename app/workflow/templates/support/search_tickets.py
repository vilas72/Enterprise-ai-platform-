
from __future__ import annotations
from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class SearchTicketsTemplate(WorkflowTemplate):

    def __init__(self):
        super().__init__(
            capability="search_tickets",
            name="Search Support Tickets",
            description="Search Jira support tickets.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                    id="search_tickets",
                    name="Search Tickets",
                    agent="support",
                    capability="search_tickets",
                    action=ActionType.FETCH_TICKET,
                )
            ],
        )