from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class SuccessCriteria(BaseModel):
    """
    Defines measurable success criteria for a Goal.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    name: str

    description: str | None = None

    satisfied: bool = False

    def mark_satisfied(self) -> None:
        self.satisfied = True