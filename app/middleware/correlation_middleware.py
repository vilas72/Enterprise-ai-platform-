from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.request_context import RequestContext


class CorrelationMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsible for managing request correlation IDs.

    Responsibilities:
    - Read X-Correlation-ID from incoming requests.
    - Generate a new UUID if one is not provided.
    - Store the correlation ID in RequestContext.
    - Add the correlation ID to the response headers.
    - Clear the request context after the request completes.
    """

    HEADER_NAME = "X-Correlation-ID"

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        correlation_id = request.headers.get(self.HEADER_NAME)

        if not correlation_id:
            correlation_id = str(uuid4())

        RequestContext.set_correlation_id(correlation_id)

        try:
            response = await call_next(request)

            response.headers[self.HEADER_NAME] = correlation_id

            return response

        finally:
            RequestContext.clear()