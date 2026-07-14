from __future__ import annotations

from app.agent.multi_agent.models.agent_descriptor import AgentDescriptor
from app.agent.multi_agent.models.agent_task import (
    AgentTask,
)
from app.agent.multi_agent.models.collaboration_request import (
    CollaborationRequest,
)


class TaskRouter:
    """
    Responsible for converting a collaboration request into
    executable agent tasks.

    The router intentionally does NOT perform planning.

    Planning remains the responsibility of the existing
    Planner inside the Agent Runtime.

    The router simply determines what work should be sent
    to each participating agent.
    """

    def route(
        self,
        request: CollaborationRequest,
        agents: list[AgentDescriptor],
    ) -> list[AgentTask]:
        """
        Create one task for each selected agent.
        """

        tasks: list[AgentTask] = []

        for agent in agents:

            task = AgentTask(
                title=f"{agent.name} Task",
                instruction=request.query,
                required_capabilities=agent.capabilities,
                correlation_id=request.collaboration_id,
                input_data=request.context.copy(),
                metadata=request.metadata.copy(),
            )

            task.assign(agent.agent_id)

            tasks.append(task)

        return tasks

    def route_for_agent(
        self,
        request: CollaborationRequest,
        agent: AgentDescriptor,
    ) -> AgentTask:
        """
        Create a task for a single agent.
        """

        task = AgentTask(
            title=f"{agent.name} Task",
            instruction=request.query,
            required_capabilities=agent.capabilities,
            correlation_id=request.collaboration_id,
            input_data=request.context.copy(),
            metadata=request.metadata.copy(),
        )

        task.assign(agent.agent_id)

        return task

    def group_by_agent(
        self,
        tasks: list[AgentTask],
    ) -> dict[str, list[AgentTask]]:
        """
        Group tasks by assigned agent.
        """

        grouped: dict[str, list[AgentTask]] = {}

        for task in tasks:

            if task.assigned_agent_id is None:
                continue

            grouped.setdefault(
                task.assigned_agent_id,
                [],
            ).append(task)

        return grouped