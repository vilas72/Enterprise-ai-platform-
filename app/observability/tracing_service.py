from __future__ import annotations

import asyncio
from collections import deque

from app.observability.models import ExecutionTrace


class TracingService:
    """
    Stores execution traces for runtime observability.

    The service maintains a bounded in-memory trace history that can
    be consumed by dashboards, health endpoints, diagnostics, and
    future persistent trace exporters.

    This service contains no business logic.
    """

    DEFAULT_TRACE_HISTORY = 1000

    def __init__(
        self,
        max_history: int = DEFAULT_TRACE_HISTORY,
    ) -> None:
        self._lock = asyncio.Lock()
        self._traces: deque[ExecutionTrace] = deque(maxlen=max_history)

    async def record(
        self,
        trace: ExecutionTrace,
    ) -> None:
        """
        Records a completed execution trace.
        """

        async with self._lock:
            self._traces.append(trace)

    async def get_trace(
        self,
        trace_id: str,
    ) -> ExecutionTrace | None:
        """
        Returns a trace by its identifier.
        """

        async with self._lock:
            for trace in self._traces:
                if trace.trace_id == trace_id:
                    return trace

        return None

    async def get_execution_traces(
        self,
        execution_id: str,
    ) -> list[ExecutionTrace]:
        """
        Returns all traces belonging to an execution.
        """

        async with self._lock:
            return [
                trace
                for trace in self._traces
                if trace.execution_id == execution_id
            ]

    async def get_conversation_traces(
        self,
        conversation_id: str,
    ) -> list[ExecutionTrace]:
        """
        Returns all traces for a conversation.
        """

        async with self._lock:
            return [
                trace
                for trace in self._traces
                if trace.conversation_id == conversation_id
            ]

    async def get_component_traces(
        self,
        component: str,
    ) -> list[ExecutionTrace]:
        """
        Returns traces for a runtime component.
        """

        async with self._lock:
            return [
                trace
                for trace in self._traces
                if trace.component == component
            ]

    async def list_traces(
        self,
        *,
        limit: int | None = None,
    ) -> list[ExecutionTrace]:
        """
        Returns recorded traces ordered from newest to oldest.
        """

        async with self._lock:
            traces = list(reversed(self._traces))

        if limit is not None:
            return traces[:limit]

        return traces

    async def delete_trace(
        self,
        trace_id: str,
    ) -> bool:
        """
        Deletes a trace if it exists.

        Returns:
            True if removed, otherwise False.
        """

        async with self._lock:
            for trace in list(self._traces):
                if trace.trace_id == trace_id:
                    self._traces.remove(trace)
                    return True

        return False

    async def clear(
        self,
    ) -> None:
        """
        Removes all recorded traces.
        """

        async with self._lock:
            self._traces.clear()

    async def count(
        self,
    ) -> int:
        """
        Returns the number of stored traces.
        """

        async with self._lock:
            return len(self._traces)