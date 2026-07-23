"""
Workflow Template Registry.
"""

from __future__ import annotations

from app.workflow.templates.workflow_template import WorkflowTemplate


class WorkflowTemplateRegistry:
    """
    Registry for reusable workflow templates.

    Templates are registered during application startup and are
    retrieved by capability when building executable workflows.
    """

    def __init__(self) -> None:
        self._templates: dict[str, WorkflowTemplate] = {}

    def register(
        self,
        template: WorkflowTemplate,
    ) -> None:
        """
        Register a workflow template.

        Raises:
            ValueError:
                If a template for the capability is already registered.
        """
        capability = template.capability.lower()

        if capability in self._templates:
            raise ValueError(
                f"Workflow template already registered for capability "
                f"'{template.capability}'."
            )

        self._templates[capability] = template

    def unregister(
        self,
        capability: str,
    ) -> None:
        """
        Remove a workflow template.
        """
        self._templates.pop(capability.lower(), None)

    def get(
        self,
        capability: str,
    ) -> WorkflowTemplate:
        """
        Retrieve a workflow template.

        Raises:
            KeyError:
                If no template exists for the capability.
        """
        key = capability.lower()

        if key not in self._templates:
            raise KeyError(
                f"No workflow template registered for capability "
                f"'{capability}'."
            )

        return self._templates[key]

    def exists(
        self,
        capability: str,
    ) -> bool:
        """
        Determine whether a template exists.
        """
        return capability.lower() in self._templates

    def list(
        self,
    ) -> list[WorkflowTemplate]:
        """
        Return all registered templates.
        """
        return list(self._templates.values())

    def capabilities(
        self,
    ) -> list[str]:
        """
        Return all registered capabilities.
        """
        return sorted(self._templates.keys())

    def clear(
        self,
    ) -> None:
        """
        Remove all registered templates.
        """
        self._templates.clear()

    @property
    def count(
        self,
    ) -> int:
        """
        Number of registered templates.
        """
        return len(self._templates)