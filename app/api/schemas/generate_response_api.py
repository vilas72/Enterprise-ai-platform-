from pydantic import BaseModel


class GenerateResponseAPI(BaseModel):

    provider: str

    model: str

    response: str

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    latency_ms: float