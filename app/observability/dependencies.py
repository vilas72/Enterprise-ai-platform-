from __future__ import annotations

import logging
from functools import lru_cache

from app.observability.execution_logger import ExecutionLogger
from app.observability.metrics_service import MetricsService
from app.observability.runtime_monitor import RuntimeMonitor
from app.observability.telemetry_service import TelemetryService
from app.observability.tracing_service import TracingService


@lru_cache(maxsize=1)
def get_tracing_service() -> TracingService:
    """
    Returns the singleton TracingService.
    """
    return TracingService()


@lru_cache(maxsize=1)
def get_metrics_service() -> MetricsService:
    """
    Returns the singleton MetricsService.
    """
    return MetricsService()


@lru_cache(maxsize=1)
def get_execution_logger() -> ExecutionLogger:
    """
    Returns the singleton ExecutionLogger.
    """
    logger = logging.getLogger("enterprise_ai.observability")
    return ExecutionLogger(logger)


@lru_cache(maxsize=1)
def get_telemetry_service() -> TelemetryService:
    """
    Returns the singleton TelemetryService.
    """
    return TelemetryService(
        tracing_service=get_tracing_service(),
        metrics_service=get_metrics_service(),
        execution_logger=get_execution_logger(),
    )


@lru_cache(maxsize=1)
def get_runtime_monitor() -> RuntimeMonitor:
    """
    Returns the singleton RuntimeMonitor.
    """
    return RuntimeMonitor(
        metrics_service=get_metrics_service(),
        tracing_service=get_tracing_service(),
    )