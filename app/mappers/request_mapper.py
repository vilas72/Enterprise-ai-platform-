from app.api.schemas.generate_request_api import GenerateRequestApi
from app.domain.generate_request import GenerateRequest
from app.domain.models.chat_message import ChatMessage


class RequestMapper:
    """
    Maps API request models to domain request models.
    """

    @staticmethod
    def to_domain(
        request: GenerateRequestApi,
    ) -> GenerateRequest:

        messages = [
            ChatMessage(
                role=message.role,
                content=message.content,
            )
            for message in request.messages
        ]

        return GenerateRequest(
            provider=request.provider,
            model=request.model,
            prompt=request.prompt,
            messages=messages,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )