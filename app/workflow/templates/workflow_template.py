"""
Workflow Template Model.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.workflow.models.workflow_step import WorkflowStep


class WorkflowTemplate(BaseModel):
    """
    Defines a reusable workflow template.

    A template describes the structure of a workflow for a
    specific capability. It is immutable and serves as the
    blueprint from which executable WorkflowDefinitions
    are created by the WorkflowBuilder.
    """

    capability: str = Field(
        description="Capability served by this workflow template.",
    )

    name: str = Field(
        description="Template name.",
    )

    description: str = Field(
        default="",
        description="Template description.",
    )

    version: str = Field(
        default="1.0.0",
        description="Workflow template version.",
    )

    steps: list[WorkflowStep] = Field(
        default_factory=list,
        description="Workflow steps.",
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Optional template metadata.",
    )

    def add_step(
        self,
        step: WorkflowStep,
    ) -> None:
        """
        Add a workflow step.
        """
        self.steps.append(step)

    @property
    def step_count(self) -> int:
        """
        Return the total number of workflow steps.
        """
        return len(self.steps)