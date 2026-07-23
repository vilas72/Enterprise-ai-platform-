from fastapi import logger

from app.workflow.hooks.workflow_hook import WorkflowHook
from app.workflow.models.workflow_context import WorkflowContext
from app.workflow.models.workflow_definition import WorkflowDefinition


class LoggingWorkflowHook(WorkflowHook):

    async def before_workflow(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
    ) -> None:
        logger.info(
            "Starting workflow execution: %s",
            context.execution_id,   
        )