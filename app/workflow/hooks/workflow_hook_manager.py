from fastapi import logger

from app.workflow.hooks.workflow_hook import WorkflowHook
from app.workflow.models.workflow_context import WorkflowContext
from app.workflow.models.workflow_definition import WorkflowDefinition


class WorkflowHookManager:
    
    def __init__(self) -> None:
        self._hooks: dict[str, WorkflowHook] = {}

    def register_hook(
        self,
        hook: WorkflowHook,
    ) -> None:
        logger.info(
            "Registering workflow hook '%s'.",
            hook.name,
        )

        self._hooks[hook.name] = hook

    async def before_workflow(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
    ) -> None:
        for hook in self._hooks.values():
            await hook.before_workflow(
                workflow=workflow,
                context=context,
            )

    async def after_workflow(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
    ) -> None:
        for hook in self._hooks.values():
            await hook.after_workflow(
                workflow=workflow,
                context=context,
            )

    async def before_step(
        self,
        context: WorkflowContext,
        step_id: str,
    ) -> None:
        for hook in self._hooks.values():
            await hook.before_step(
                context=context,
                step_id=step_id,
            )

    async def after_step(
        self,
        context: WorkflowContext,
        step_id: str,
    ) -> None:
        for hook in self._hooks.values():
            await hook.after_step(
                context=context,
                step_id=step_id,
            )