from app.bootstrap.provider_bootstrap import register_providers
from app.core.config import settings

from fastapi import FastAPI

from app.core.logging.config import configure_logging

from app.api.routers.ai_router import router as ai_router
from app.api.routers.health_router import router as health_router

from app.api.routers.provider_router import router as provider_router

from app.middleware.correlation_middleware import CorrelationMiddleware

from app.api.exception_handlers.global_exception_handler import (
    register_exception_handlers,
)

from app.api.routers.conversation_router import (
    router as conversation_router,
)

from app.core.logging.logger import get_logger

configure_logging()

logger = get_logger(__name__)

app = FastAPI(
    title="Enterprise AI Platform",
    version="1.0.0",
)
app.add_middleware(CorrelationMiddleware)

app.include_router(health_router)
app.include_router(ai_router)
app.include_router(provider_router)
app.include_router(conversation_router)

register_exception_handlers(app)


def main():
    logger.info("Starting Enterprise AI Platform...")

    register_providers()

    logger.info("Provider registration completed.")
    logger.info(f"Default Provider : {settings.default_provider}")
    logger.info("Application initialized successfully.")

if __name__ == "__main__":
    main()