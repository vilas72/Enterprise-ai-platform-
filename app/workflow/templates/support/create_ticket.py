"""
Support Ticket Creation Workflow Template.
"""

from __future__ import annotations
from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class CreateTicketTemplate(WorkflowTemplate):
    """
    Workflow template for creating enterprise support tickets.

    Workflow:
        Create Ticket
              ↓
                      
    """

    def __init__(self) -> None:
        super().__init__(
            capability="create_ticket",
            name="Create Support Ticket",
            description="Create an enterprise support ticket.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                     id="create_ticket",
                    name="Create Ticket",
                    agent="support",
                    capability="create_ticket",
                    action=ActionType.CREATE_TICKET,
                ) 
            ],
        )

