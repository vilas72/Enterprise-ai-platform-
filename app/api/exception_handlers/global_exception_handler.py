from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.ai_provider_exception import AIProviderException


def register_exception_handlers(app):

    @app.exception_handler(AIProviderException)
    async def ai_provider_exception_handler(
        request: Request,
        exc: AIProviderException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                },
            },
        )