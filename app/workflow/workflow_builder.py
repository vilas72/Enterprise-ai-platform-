"""
Workflow Builder.
"""

from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

from app.agents.planner.planner_result import PlannerResult
from app.workflow.models.workflow_definition import WorkflowDefinition
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template_registry import (
    WorkflowTemplateRegistry,
)


class WorkflowBuilder:
    """
    Builds executable workflow definitions from reusable
    workflow templates.
    """

    def __init__(
        self,
        registry: WorkflowTemplateRegistry,
    ) -> None:
        self._registry = registry

    def build(
        self,
        planner_result: PlannerResult,
    ) -> WorkflowDefinition:
        """
        Build an executable workflow.
        """

        workflow_capability = planner_result.workflow_capability

        if not self._registry.exists(workflow_capability):
                raise ValueError(
                    f"No workflow template registered for "
                    f"workflow capability '{workflow_capability}'."
                )

        template = self._registry.get(
            workflow_capability
        )

        workflow = WorkflowDefinition(
            id=str(uuid4()),
            name=template.name,
            description=template.description,
            version=template.version,
            steps=self._build_steps(
                template.steps,
                planner_result,
            ),
            metadata={
                **template.metadata,
                "requested_capability": planner_result.requested_capability,
                "workflow_capability": planner_result.workflow_capability,
                "planner": planner_result.planner,
                "selected_agent": planner_result.selected_agent,
                "confidence": planner_result.payload.get("confidence"),
            },
        )

        return workflow

    def _build_steps(
        self,
        template_steps: list[WorkflowStep],
        planner_result: PlannerResult,
    ) -> list[WorkflowStep]:
        """
        Clone workflow template steps.
        """

        workflow_steps: list[WorkflowStep] = []

        for step in template_steps:

            cloned_step = deepcopy(step)
            
            if planner_result.payload:
                cloned_step.inputs = {
                    **(cloned_step.inputs or {}),
                    **(planner_result.payload or {}),
                }


            workflow_steps.append(
                cloned_step,
            )

        return workflow_steps