from __future__ import annotations

from datetime import datetime, timezone

from app.observability.metrics_service import MetricsService
from app.observability.models import RuntimeSnapshot
from app.observability.tracing_service import TracingService


class RuntimeMonitor:
    """
    Provides aggregated runtime statistics for monitoring, health
    endpoints, dashboards, and operational diagnostics.

    This service derives runtime statistics from the observability
    services and does not own business state.
    """

    def __init__(
        self,
        metrics_service: MetricsService,
        tracing_service: TracingService,
    ) -> None:
        self._metrics = metrics_service
        self._tracing = tracing_service

    async def get_snapshot(self) -> RuntimeSnapshot:
        """
        Returns the current runtime snapshot.
        """

        counters = await self._metrics.get_all_counters()
        traces = await self._tracing.list_traces()

        average_latency = 0.0
        if traces:
            durations = [
                trace.duration_ms
                for trace in traces
                if trace.duration_ms is not None
            ]
            if durations:
                average_latency = sum(durations) / len(durations)

        active_conversations = len(
            {
                trace.conversation_id
                for trace in traces
            }
        )

        active_agents = len(
            {
                trace.execution_id
                for trace in traces
                if trace.component.lower().startswith("agent")
            }
        )

        active_tools = len(
            {
                trace.operation
                for trace in traces
                if trace.component.lower().startswith("tool")
            }
        )

        return RuntimeSnapshot(
            timestamp=datetime.now(timezone.utc),
            active_conversations=active_conversations,
            active_agents=active_agents,
            active_tools=active_tools,
            requests_total=int(
                counters.get("executions.total", 0)
            ),
            failures_total=int(
                counters.get("executions.failed", 0)
            ),
            average_latency_ms=round(
                average_latency,
                3,
            ),
        )

    async def get_success_rate(self) -> float:
        """
        Returns the overall execution success rate as a percentage.
        """

        counters = await self._metrics.get_all_counters()

        total = counters.get("executions.total", 0)
        success = counters.get("executions.success", 0)

        if total == 0:
            return 100.0

        return round((success / total) * 100, 2)

    async def get_failure_rate(self) -> float:
        """
        Returns the overall execution failure rate as a percentage.
        """

        counters = await self._metrics.get_all_counters()

        total = counters.get("executions.total", 0)
        failed = counters.get("executions.failed", 0)

        if total == 0:
            return 0.0

        return round((failed / total) * 100, 2)

    async def get_component_summary(self) -> dict[str, dict[str, float | int]]:
        """
        Returns execution statistics grouped by runtime component.
        """

        traces = await self._tracing.list_traces()

        summary: dict[str, dict[str, float | int]] = {}

        for trace in traces:
            component = trace.component

            if component not in summary:
                summary[component] = {
                    "executions": 0,
                    "success": 0,
                    "failed": 0,
                    "average_latency_ms": 0.0,
                    "_latency_total": 0.0,
                }

            item = summary[component]

            item["executions"] += 1

            if trace.success:
                item["success"] += 1
            else:
                item["failed"] += 1

            if trace.duration_ms is not None:
                item["_latency_total"] += trace.duration_ms

        for component, item in summary.items():
            executions = item["executions"]

            if executions:
                item["average_latency_ms"] = round(
                    item["_latency_total"] / executions,
                    3,
                )

            item.pop("_latency_total", None)

        return summary