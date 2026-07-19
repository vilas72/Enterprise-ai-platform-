"""
Runtime Context Models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.gateway.models import GatewayRequest


class RuntimeContext(BaseModel):
    """
    Shared runtime execution context.
    """
    execution_id: str
    workflow_id: str | None = None
    agent: str
    
    request: GatewayRequest
    capability: str


    response: Any | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)

    def set_variable(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a runtime variable.
        """

        self.variables[key] = value

    def get_variable(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a runtime variable.
        """

        return self.variables.get(
            key,
            default,
        )