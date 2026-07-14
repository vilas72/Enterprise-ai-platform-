from __future__ import annotations

import asyncio
import time
from typing import Protocol

from app.agent.multi_agent.models.agent_task import (
    AgentTask,
)
from app.agent.multi_agent.models.collaboration_result import (
    CollaborationResult,
    CollaborationStatus,
)


class AgentExecutor(Protocol):
    """
    Contract implemented by the existing Agent Runtime.

    The concrete implementation will adapt the platform's
    AgentRuntime to the Multi-Agent Runtime.
    """

    async def execute(
        self,
        task: AgentTask,
    ) -> object:
        ...


class TaskDispatcher:
    """
    Dispatches AgentTasks to the underlying Agent Runtime.

    Responsibilities:

    - Parallel execution
    - Task lifecycle updates
    - Failure isolation
    - Result creation

    This class intentionally performs no planning or routing.
    """

    def __init__(
        self,
        executor: AgentExecutor,
    ) -> None:
        self._executor = executor

    async def dispatch(
        self,
        tasks: list[AgentTask],
    ) -> list[CollaborationResult]:
        """
        Execute all tasks concurrently.
        """

        if not tasks:
            return []

        return await asyncio.gather(
            *[
                self._dispatch_task(task)
                for task in tasks
            ]
        )

    async def dispatch_one(
        self,
        task: AgentTask,
    ) -> CollaborationResult:
        """
        Execute a single task.
        """

        return await self._dispatch_task(task)

    async def _dispatch_task(
        self,
        task: AgentTask,
    ) -> CollaborationResult:

        started = time.perf_counter()

        try:

            task.mark_running()

            result = await self._executor.execute(task)

            task.mark_completed()

            duration = (
                time.perf_counter() - started
            ) * 1000

            return CollaborationResult(
                task_id=task.task_id,
                agent_id=task.assigned_agent_id or "",
                status=CollaborationStatus.SUCCESS,
                output=result,
                execution_time_ms=duration,
            )

        except Exception as ex:

            task.mark_failed()

            duration = (
                time.perf_counter() - started
            ) * 1000

            return CollaborationResult(
                task_id=task.task_id,
                agent_id=task.assigned_agent_id or "",
                status=CollaborationStatus.FAILED,
                output=None,
                reasoning=str(ex),
                execution_time_ms=duration,
                metadata={
                    "exception": ex.__class__.__name__,
                },
            )