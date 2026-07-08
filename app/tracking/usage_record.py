from datetime import datetime

from pydantic import BaseModel, Field


class UsageRecord(BaseModel):
    """
    Represents one AI request usage record.
    """

    provider: str

    model: str

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    latency_ms: float

    estimated_cost: float = 0.0

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )