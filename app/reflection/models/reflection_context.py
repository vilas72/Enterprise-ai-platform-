"""
Reflection Context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ReflectionContext:
    """
    Reflection execution context.
    """

    workflow_id: str

    execution_id: str

    event_type: str

    event_payload: dict[str, Any] = field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    variables: dict[str, Any] = field(
        default_factory=dict,
    )

    def set_variable(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.variables[key] = value

    def get_variable(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.variables.get(
            key,
            default,
        )