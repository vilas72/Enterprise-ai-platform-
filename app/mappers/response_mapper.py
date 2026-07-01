from app.api.schemas.generate_response_api import GenerateResponseAPI
from app.domain.generate_response import GenerateResponse


class ResponseMapper:

    @staticmethod
    def to_api(
        response: GenerateResponse,
    ) -> GenerateResponseAPI:

        return GenerateResponseAPI(
            provider=response.provider,
            model=response.model,
            response=response.response,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            total_tokens=response.total_tokens,
            latency_ms=response.latency_ms,
        )