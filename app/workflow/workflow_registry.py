"""
Workflow Registry.
"""

from __future__ import annotations

from app.workflow.models.workflow_definition import WorkflowDefinition


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

        self._workflows[workflow.id] = workflow

    def get(
        self,
        workflow_id: str,
    ) -> WorkflowDefinition:
        """
        Retrieve a workflow.
        """

        return self._workflows[workflow_id]

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

        self._workflows.pop(workflow_id, None)