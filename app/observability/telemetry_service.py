from __future__ import annotations

import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncIterator
from uuid import uuid4

from app.observability.models import ExecutionTrace
from app.observability.tracing_service import TracingService
from app.observability.metrics_service import MetricsService
from app.observability.execution_logger import ExecutionLogger


class TelemetryService:
    """
    Central observability service responsible for recording execution traces,
    runtime metrics, and structured execution logs.

    This service is intentionally lightweight and contains no business logic.
    It can be safely reused across AI Runtime, Tool Runtime, Agent Runtime,
    Multi-Agent Runtime, and Agentic Runtime.
    """

    def __init__(
        self,
        tracing_service: TracingService,
        metrics_service: MetricsService,
        execution_logger: ExecutionLogger,
    ) -> None:
        self._tracing = tracing_service
        self._metrics = metrics_service
        self._logger = execution_logger

    @asynccontextmanager
    async def trace(
        self,
        *,
        conversation_id: str,
        execution_id: str,
        component: str,
        operation: str,
        metadata: dict[str, Any] | None = None,
    ) -> AsyncIterator[ExecutionTrace]:
        """
        Context manager used to automatically trace an execution.

        Example:
            async with telemetry.trace(...):
                await executor.execute(...)
        """

        trace = ExecutionTrace(
            trace_id=str(uuid4()),
            conversation_id=conversation_id,
            execution_id=execution_id,
            component=component,
            operation=operation,
            started_at=datetime.now(timezone.utc),
            metadata=metadata or {},
        )

        started = time.perf_counter()

        try:
            yield trace

            trace.success = True

        except Exception as exc:
            trace.success = False
            trace.error = str(exc)
            raise

        finally:
            trace.completed_at = datetime.now(timezone.utc)
            trace.duration_ms = round(
                (time.perf_counter() - started) * 1000,
                3,
            )

            await self._tracing.record(trace)

            await self._metrics.record_execution(
                component=trace.component,
                operation=trace.operation,
                duration_ms=trace.duration_ms,
                success=trace.success,
            )

            await self._logger.log_execution(trace)

    async def record_event(
        self,
        *,
        component: str,
        event: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Records a runtime event that is not associated with an execution trace.
        """

        await self._logger.log_event(
            component=component,
            event=event,
            metadata=metadata or {},
        )

    async def increment_counter(
        self,
        *,
        name: str,
        labels: dict[str, str] | None = None,
        value: float = 1,
    ) -> None:
        """
        Increment a named counter metric.
        """

        await self._metrics.increment(
            name=name,
            value=value,
            labels=labels or {},
        )

    async def record_metric(
        self,
        *,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Record an arbitrary metric.
        """

        await self._metrics.record(
            name=name,
            value=value,
            labels=labels or {},
        )