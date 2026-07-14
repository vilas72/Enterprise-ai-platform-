from __future__ import annotations

from logging import Logger
from typing import Any

from app.observability.models import ExecutionTrace


class ExecutionLogger:
    """
    Structured execution logger for the Enterprise Agentic AI Platform.

    This service emits structured log records that can be consumed by
    existing logging infrastructure (console, file, ELK, Azure Monitor,
    CloudWatch, Datadog, Splunk, etc.).

    It does not own log configuration—it only formats runtime events.
    """

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    async def log_execution(
        self,
        trace: ExecutionTrace,
    ) -> None:
        """
        Log a completed execution trace.
        """

        payload = {
            "trace_id": trace.trace_id,
            "conversation_id": trace.conversation_id,
            "execution_id": trace.execution_id,
            "component": trace.component,
            "operation": trace.operation,
            "success": trace.success,
            "duration_ms": trace.duration_ms,
            "started_at": trace.started_at.isoformat(),
            "completed_at": (
                trace.completed_at.isoformat()
                if trace.completed_at
                else None
            ),
            "metadata": trace.metadata,
            "error": trace.error,
        }

        if trace.success:
            self._logger.info(
                "Execution completed",
                extra={"execution": payload},
            )
        else:
            self._logger.error(
                "Execution failed",
                extra={"execution": payload},
            )

    async def log_event(
        self,
        *,
        component: str,
        event: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Log a runtime event.
        """

        self._logger.info(
            "Runtime event",
            extra={
                "event": {
                    "component": component,
                    "name": event,
                    "metadata": metadata or {},
                }
            },
        )

    async def log_warning(
        self,
        *,
        component: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Log a warning.
        """

        self._logger.warning(
            message,
            extra={
                "warning": {
                    "component": component,
                    "metadata": metadata or {},
                }
            },
        )

    async def log_error(
        self,
        *,
        component: str,
        message: str,
        exception: Exception | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Log an error.
        """

        self._logger.error(
            message,
            exc_info=exception,
            extra={
                "error": {
                    "component": component,
                    "exception": (
                        type(exception).__name__
                        if exception
                        else None
                    ),
                    "metadata": metadata or {},
                }
            },
        )

    async def log_debug(
        self,
        *,
        component: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Log debug information.
        """

        self._logger.debug(
            message,
            extra={
                "debug": {
                    "component": component,
                    "metadata": metadata or {},
                }
            },
        )