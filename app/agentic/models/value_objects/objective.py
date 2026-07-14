from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Objective(BaseModel):
    """
    A single business objective belonging to a Goal.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    name: str

    description: str | None = None

    completed: bool = False

    order: int = Field(
        default=1,
        ge=1,
    )

    def mark_completed(self) -> None:
        self.completed = True