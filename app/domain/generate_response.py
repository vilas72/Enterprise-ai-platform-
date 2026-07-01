from pydantic import BaseModel


class GenerateResponse(BaseModel):

    provider: str

    model: str

    response: str

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    latency_ms: float = 0