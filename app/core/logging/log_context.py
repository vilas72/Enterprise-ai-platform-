from __future__ import annotations

from typing import Any

from app.core.request_context import RequestContext


class LogContext:
    """
    Provides common logging context for the Enterprise AI Platform.

    This class centralizes contextual information that can be
    attached to log records.

    Future extensions:
        - User ID
        - Tenant ID
        - Trace ID
        - Span ID
        - Session ID
        - Conversation ID
    """

    @staticmethod
    def correlation_id() -> str:
        """
        Returns the current request correlation ID.
        """

        return RequestContext.get_correlation_id() or "-"

    @staticmethod
    def common() -> dict[str, Any]:
        """
        Returns common logging context shared by all log messages.
        """

        return {
            "correlation_id": LogContext.correlation_id(),
        }

    @staticmethod
    def provider(
        provider: str,
        model: str | None = None,
    ) -> dict[str, Any]:
        """
        Logging context for AI provider operations.
        """

        context = LogContext.common()

        context.update(
            {
                "provider": provider,
                "model": model or "-",
            }
        )

        return context

    @staticmethod
    def request(
        method: str,
        endpoint: str,
    ) -> dict[str, Any]:
        """
        Logging context for HTTP requests.
        """

        context = LogContext.common()

        context.update(
            {
                "method": method,
                "endpoint": endpoint,
            }
        )

        return context

    @staticmethod
    def exception(
        exception_type: str,
    ) -> dict[str, Any]:
        """
        Logging context for exception events.
        """

        context = LogContext.common()

        context.update(
            {
                "exception_type": exception_type,
            }
        )

        return context