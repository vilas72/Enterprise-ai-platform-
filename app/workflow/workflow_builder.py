"""
Workflow Builder.
"""

from __future__ import annotations

from app.agents.planner.planner_result import PlannerResult
from app.workflow.models.workflow_definition import (
    WorkflowDefinition,
    WorkflowType,
)
from app.workflow.models.workflow_step import (
    WorkflowStep,
    WorkflowStepType,
)


class WorkflowBuilder:
    """
    Builds executable workflows from planner results.
    """

    def build(
        self,
        planner_result: PlannerResult,
    ) -> WorkflowDefinition:
        """
        Build a workflow definition from the planner result.
        """

        steps = []

        for index, planner_step in enumerate(
            planner_result.workflow,
            start=1,
        ):
            step = WorkflowStep(
                id=f"step-{planner_step.order}",
                name=planner_step.capability.replace("_", " ").title(),
                description=f"Execute '{planner_step.capability}' using '{planner_step.agent}'",
                type=WorkflowStepType.TASK,
                agent=planner_step.agent,
                capability=planner_step.capability,
                inputs=planner_step.payload,
                metadata={},
            )

            steps.append(step)

        workflow_type = (
            WorkflowType.SINGLE_AGENT
            if len(steps) == 1
            else WorkflowType.MULTI_AGENT
        )

        return WorkflowDefinition(
            id=planner_result.capability,
            name=planner_result.capability.replace(
                "_",
                " ",
            ).title(),
            description=planner_result.reasoning,
            type=workflow_type,
            steps=steps,
            metadata={
                "planner": planner_result.planner,
                "confidence": planner_result.confidence,
                "selected_agent": planner_result.selected_agent,
            },
        )