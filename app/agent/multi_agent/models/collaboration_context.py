from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.agent.multi_agent.models.agent_task import AgentTask


class CollaborationContext(BaseModel):
    """
    Shared execution context.

    This object is mutable during orchestration.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    collaboration_id: str

    variables: dict[str, Any] = Field(
        default_factory=dict,
    )

    shared_memory: dict[str, Any] = Field(
        default_factory=dict,
    )

    tasks: list[AgentTask] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )

    def add_task(self, task: AgentTask) -> None:
        self.tasks.append(task)

    def set_variable(self, key: str, value: Any) -> None:
        self.variables[key] = value

    def get_variable(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.variables.get(key, default)