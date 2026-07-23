"""
Support Ticket Resolution Workflow Template.
"""

from __future__ import annotations
from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class GenerateRcaTemplate(WorkflowTemplate):
    """
    Workflow template for generating root cause analysis for enterprise support tickets.

    Workflow:

        Fetch Ticket
                ↓
        Analyze Root Cause

    """

    def __init__(self) -> None:
        super().__init__(
            capability="generate_rca",
            name="Generate Root Cause Analysis",
            description="Generate root cause analysis for an enterprise support ticket.",
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
                    id="analyze_root_cause",
                    name="Analyze Root Cause",
                    agent="support",
                    capability="analyze_root_cause",
                    action=ActionType.ANALYZE_ROOT_CAUSE,
                    depends_on=["search_knowledge"],
                ),
            ],
        )

