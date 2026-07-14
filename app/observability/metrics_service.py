from __future__ import annotations

import asyncio
from collections import defaultdict
from datetime import datetime, timezone

from app.observability.models import MetricRecord


class MetricsService:
    """
    Collects in-memory runtime metrics for the platform.

    This service is intentionally lightweight and async-safe.
    It serves as the single source of runtime metrics for
    observability, dashboards, and future metric exporters.
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()

        self._metrics: list[MetricRecord] = []

        self._counters: dict[str, float] = defaultdict(float)

        self._latency_sum: dict[str, float] = defaultdict(float)

        self._latency_count: dict[str, int] = defaultdict(int)

    async def increment(
        self,
        *,
        name: str,
        value: float = 1,
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Increment a counter metric.
        """

        async with self._lock:
            self._counters[name] += value

            self._metrics.append(
                MetricRecord(
                    name=name,
                    value=self._counters[name],
                    timestamp=datetime.now(timezone.utc),
                    labels=labels or {},
                )
            )

    async def record(
        self,
        *,
        name: str,
        value: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Record a metric sample.
        """

        async with self._lock:
            self._metrics.append(
                MetricRecord(
                    name=name,
                    value=value,
                    timestamp=datetime.now(timezone.utc),
                    labels=labels or {},
                )
            )

    async def record_execution(
        self,
        *,
        component: str,
        operation: str,
        duration_ms: float,
        success: bool,
    ) -> None:
        """
        Records execution latency and outcome.
        """

        key = f"{component}.{operation}"

        async with self._lock:
            self._latency_sum[key] += duration_ms
            self._latency_count[key] += 1

            self._metrics.append(
                MetricRecord(
                    name="execution.duration",
                    value=duration_ms,
                    timestamp=datetime.now(timezone.utc),
                    labels={
                        "component": component,
                        "operation": operation,
                        "success": str(success).lower(),
                    },
                )
            )

            self._counters["executions.total"] += 1

            if success:
                self._counters["executions.success"] += 1
            else:
                self._counters["executions.failed"] += 1

    async def get_counter(
        self,
        name: str,
    ) -> float:
        """
        Returns a counter value.
        """

        async with self._lock:
            return self._counters.get(name, 0.0)

    async def get_average_latency(
        self,
        component: str,
        operation: str,
    ) -> float:
        """
        Returns average execution latency.
        """

        key = f"{component}.{operation}"

        async with self._lock:
            count = self._latency_count.get(key, 0)

            if count == 0:
                return 0.0

            return self._latency_sum[key] / count

    async def get_all_counters(
        self,
    ) -> dict[str, float]:
        """
        Returns all counters.
        """

        async with self._lock:
            return dict(self._counters)

    async def get_metrics(
        self,
    ) -> list[MetricRecord]:
        """
        Returns all collected metric samples.
        """

        async with self._lock:
            return list(self._metrics)

    async def clear(
        self,
    ) -> None:
        """
        Clears all collected metrics.
        """

        async with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._latency_sum.clear()
            self._latency_count.clear()