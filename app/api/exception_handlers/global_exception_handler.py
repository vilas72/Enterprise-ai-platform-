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

    # Catch OpenAI SDK errors that escape the provider layer
    try:
        from openai import OpenAIError, PermissionDeniedError, AuthenticationError

        @app.exception_handler(PermissionDeniedError)
        async def openai_permission_handler(request: Request, exc: PermissionDeniedError):
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "error": {
                        "code": "provider_permission_denied",
                        "message": str(exc),
                        "details": "The configured API key does not have access to the requested model.",
                    },
                },
            )

        @app.exception_handler(AuthenticationError)
        async def openai_auth_handler(request: Request, exc: AuthenticationError):
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "error": {
                        "code": "provider_authentication_failed",
                        "message": str(exc),
                        "details": "Invalid or missing API key.",
                    },
                },
            )

        @app.exception_handler(OpenAIError)
        async def openai_generic_handler(request: Request, exc: OpenAIError):
            return JSONResponse(
                status_code=502,
                content={
                    "success": False,
                    "error": {
                        "code": "provider_error",
                        "message": str(exc),
                        "details": "An error occurred communicating with the AI provider.",
                    },
                },
            )

    except ImportError:
        pass  # openai not installed