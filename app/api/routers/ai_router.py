from collections.abc import Generator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.schemas.generate_request_api import GenerateRequestApi
from app.api.schemas.generate_response_api import GenerateResponseAPI
from app.dependencies.service_dependencies import get_ai_service
from app.mappers.request_mapper import RequestMapper
from app.mappers.response_mapper import ResponseMapper
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


def event_stream(
    generator: Generator[str, None, None],
):
    """
    Converts AI response generator into
    Server-Sent Events (SSE).
    """

    try:

        for chunk in generator:
            yield f"data: {chunk}\n\n"

        yield "event: complete\ndata: [DONE]\n\n"

    except Exception as ex:
        yield f"event: error\ndata: {str(ex)}\n\n"


@router.post(
    "/generate",
    response_model=GenerateResponseAPI,
    summary="Generate AI Response",
)
def generate(
    request: GenerateRequestApi,
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Generates a complete AI response.
    """

    domain_request = RequestMapper.to_domain(request)

    response = ai_service.generate(domain_request)

    return ResponseMapper.to_api(response)


@router.post(
    "/generate/stream",
    summary="Generate Streaming AI Response",
)
def generate_stream(
    request: GenerateRequestApi,
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Streams AI responses using
    Server-Sent Events (SSE).
    """

    domain_request = RequestMapper.to_domain(request)

    generator = ai_service.stream(domain_request)

    return StreamingResponse(
        event_stream(generator),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )