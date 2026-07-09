from app.domain.generate_request import GenerateRequest
from app.domain.generate_response import GenerateResponse
from app.providers.ai_provider import AIProvider


class MockProvider(AIProvider):

    def generate(self, request: GenerateRequest) -> GenerateResponse:

        return GenerateResponse(
            provider="Mock",
            model="mock-model-v1",
            response=f"Mock Response: {request.prompt}",
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
            latency_ms=5,
            finish_reason="stop",
        )