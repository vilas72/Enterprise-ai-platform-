"""
Support Ticket Update Workflow Template.
"""

from __future__ import annotations
from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class UpdateTicketTemplate(WorkflowTemplate):
    """
    Workflow template for updating enterprise support tickets.

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
      """

    def __init__(self) -> None:
        super().__init__(
            capability="update_ticket",
            name="Update Support Ticket",
            description="Update an enterprise support ticket.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                     id="update_ticket",
                    name="Update Ticket",
                    agent="support",
                    capability="update_ticket",
                    action=ActionType.UPDATE_TICKET,
                ) 
            ],
        )

