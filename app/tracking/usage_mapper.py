from app.domain.generate_response import GenerateResponse
from app.tracking.usage_record import UsageRecord


class UsageMapper:
    """
    Maps GenerateResponse to UsageRecord.
    """

    @staticmethod
    def from_generate_response(
        response: GenerateResponse,
    ) -> UsageRecord:

        return UsageRecord(
            provider=response.provider,
            model=response.model,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            total_tokens=response.total_tokens,
            latency_ms=response.latency_ms,
        )