from pydantic import BaseModel


class UsageStatisticsResponse(BaseModel):
    """
    Overall AI usage statistics.
    """

    total_requests: int

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    average_latency_ms: float

    estimated_cost: float