"""
Workflow Context Models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.gateway.models import GatewayRequest


class WorkflowContext(BaseModel):
    """
    Shared execution context for a workflow.
    """

    workflow_id: str = Field(
        description="Workflow identifier.",
    )

    execution_id: str = Field(
        description="Workflow execution identifier.",
    )

    current_step: str | None = Field(
        default=None,
        description="Current executing step.",
    )

    variables: dict[str, Any] = Field(
        default_factory=dict,
        description="Shared workflow variables.",
    )

    step_results: dict[str, Any] = Field(
        default_factory=dict,
        description="Results produced by workflow steps.",
    )
    
    request: GatewayRequest

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata.",
    )
    

    def set_variable(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a workflow variable.
        """

        self.variables[key] = value

    def get_variable(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a workflow variable.
        """

        return self.variables.get(key, default)

    def add_step_result(
        self,
        step_id: str,
        result: Any,
    ) -> None:
        """
        Store the result of a workflow step.
        """

        self.step_results[step_id] = result

    def get_step_result(
        self,
        step_id: str,
    ) -> Any:
        """
        Retrieve the result of a workflow step.
        """

        return self.step_results.get(step_id)