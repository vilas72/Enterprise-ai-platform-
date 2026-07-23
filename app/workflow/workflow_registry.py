"""
Workflow Registry.
"""

from __future__ import annotations

from app.workflow.models.workflow_definition import WorkflowDefinition

from app.workflow.exceptions import (
    WorkflowNotFoundException,
    WorkflowValidationException,
)

class WorkflowRegistry:
    """
    Registry for workflow definitions.
    """

    def __init__(self) -> None:
        self._workflows: dict[str, WorkflowDefinition] = {}

    def register(
        self,
        workflow: WorkflowDefinition,
    ) -> None:
        """
        Register a workflow.
        """

        if workflow.id in self._workflows:
            raise WorkflowValidationException(
                f"Workflow '{workflow.id}' is already registered."
            )
        
        self._workflows[workflow.id] = workflow

    def get(
        self,
        workflow_id: str,
    ) -> WorkflowDefinition:
        """
        Retrieve a workflow.
        """

        workflow = self._workflows.get(workflow_id)

        if workflow is None:
            raise WorkflowNotFoundException(
                f"Workflow '{workflow_id}' was not found."
            )

        return workflow
    
    def exists(
        self,
        workflow_id: str,
    ) -> bool:
        """
        Check whether a workflow exists.
        """

        return workflow_id in self._workflows

    def list(self) -> list[WorkflowDefinition]:
        """
        List registered workflows.
        """

        return list(self._workflows.values())

    def unregister(
        self,
        workflow_id: str,
    ) -> None:
        """
        Remove a workflow.
        """

        if workflow_id not in self._workflows:
            raise WorkflowNotFoundException(
                f"Workflow '{workflow_id}' was not found."
                
            )

        del self._workflows[workflow_id]