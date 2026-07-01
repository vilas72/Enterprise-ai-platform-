import logging

from app.core.logging.constants import PLATFORM_LOGGER_NAME


def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a child logger under the Enterprise AI Platform logger.

    Example:

        app.services.ai_service

    becomes

        enterprise_ai_platform.app.services.ai_service
    """

    logger_name = f"{PLATFORM_LOGGER_NAME}.{module_name}"

    return logging.getLogger(logger_name)