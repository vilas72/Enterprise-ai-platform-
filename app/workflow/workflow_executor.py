"""
Workflow Executor.
"""

from __future__ import annotations

from app.runtime.agent_runtime import AgentRuntime
from app.workflow.models.workflow_context import WorkflowContext
from app.workflow.models.workflow_definition import WorkflowDefinition
from app.workflow.models.workflow_result import WorkflowResult
from app.workflow.models.workflow_step import WorkflowStepStatus

from app.events.event_publisher import EventPublisher
from app.events.models.event import Event
from app.events.models.event_metadata import EventMetadata
from app.events.models.event_type import EventType

from app.workflow.hooks.workflow_hook_manager import WorkflowHookManager


class WorkflowExecutor:
    """
    Executes workflow steps sequentially.
    """

    def __init__(
        self,
        runtime: AgentRuntime,
        publisher: EventPublisher,
        hooks: WorkflowHookManager,
    ) -> None:
        self._runtime = runtime
        self._publisher = publisher
        self._hooks = hooks

    async def execute(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """
        Execute a workflow.
        """

        final_result = None

        try:

            for step in workflow.steps:

                context.current_step = step.id
                await self._hooks.before_step(
                    context=context,
                    step_id=step.id,
                )
                step.status = WorkflowStepStatus.RUNNING

                await self._publisher.publish(
                    Event(
                        event_type=EventType.STEP_STARTED,
                        metadata=EventMetadata(
                            workflow_id=context.workflow_id,
                            execution_id=context.execution_id,
                            agent=step.agent,
                            capability=step.capability,
                            source="WorkflowExecutor",
                        ),
                        payload={
                            "step_id": step.id,
                            "step_name": step.name,
                        },
                    )
                )

                runtime_result = None

                for attempt in range(step.retry_policy.max_attempts):

                    runtime_result = await self._runtime.execute(
                        agent=step.agent,
                        capability=step.capability,
                        request=context.request,
                        workflow_id=context.workflow_id,
                    )

                    if runtime_result.success:
                        break 
                
                step.outputs = {
                    "success": runtime_result.success,
                    "result": runtime_result.result,
                    "error": runtime_result.error,
                }

                # Step failed
                if not runtime_result.success:

                    step.status = WorkflowStepStatus.FAILED

                    await self._publisher.publish(
                        Event(
                            event_type=EventType.STEP_FAILED,
                            metadata=EventMetadata(
                                workflow_id=context.workflow_id,
                                execution_id=context.execution_id,
                                agent=step.agent,
                                capability=step.capability,
                                source="WorkflowExecutor",
                            ),
                            payload={
                                "step_id": step.id,
                                "step_name": step.name,
                                "error": runtime_result.error,
                            },
                        )
                    )

                    return WorkflowResult(
                        success=False,
                        workflow_id=workflow.id,
                        execution_id=context.execution_id,
                        error=runtime_result.error,
                        step_results=context.step_results,
                        metadata=context.metadata,
                    )

                # Step completed
                step.status = WorkflowStepStatus.COMPLETED

                await self._publisher.publish(
                    Event(
                        event_type=EventType.STEP_COMPLETED,
                        metadata=EventMetadata(
                            workflow_id=context.workflow_id,
                            execution_id=context.execution_id,
                            agent=step.agent,
                            capability=step.capability,
                            source="WorkflowExecutor",
                        ),
                        payload={
                            "step_id": step.id,
                            "step_name": step.name,
                            "success": True,
                        },
                    )
                )

                context.add_step_result(
                    step.id,
                    runtime_result,
                )

                context.set_variable(
                    step.id,
                    runtime_result.result,
                )

                # Save latest successful result
                final_result = runtime_result.result

            # Workflow completed successfully
            return WorkflowResult(
                success=True,
                workflow_id=workflow.id,
                execution_id=context.execution_id,
                result=final_result,
                step_results=context.step_results,
                metadata=context.metadata,
            )

        except Exception as exc:

            if context.current_step:
                for step in workflow.steps:
                    if step.id == context.current_step:
                        step.status = WorkflowStepStatus.FAILED
                        break

            await self._publisher.publish(
                Event(
                    event_type=EventType.STEP_FAILED,
                    metadata=EventMetadata(
                        workflow_id=context.workflow_id,
                        execution_id=context.execution_id,
                        source="WorkflowExecutor",
                    ),
                    payload={
                        "step_id": context.current_step,
                        "error": str(exc),
                    },
                )
            )

            return WorkflowResult(
                success=False,
                workflow_id=workflow.id,
                execution_id=context.execution_id,
                error=f"Workflow execution failed: {exc}",
                step_results=context.step_results,
                metadata=context.metadata,
            )
            
        finally:
            await self._hooks.after_step(
                context=context,
                step_id=step.id,
            )