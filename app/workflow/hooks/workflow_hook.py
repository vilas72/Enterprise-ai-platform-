from abc import ABC
from abc import abstractmethod

from app.workflow.models.workflow_context import WorkflowContext
from app.workflow.models.workflow_definition import WorkflowDefinition


class WorkflowHook(ABC):

    @abstractmethod
    async def before_workflow(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
    ) -> None:
        ...

    @abstractmethod
    async def after_workflow(
        self,
        workflow: WorkflowDefinition,
        context: WorkflowContext,
    ) -> None:
        ...

    @abstractmethod
    async def before_step(
        self,
        context: WorkflowContext,
        step_id: str,
    ) -> None:
        ...

    @abstractmethod
    async def after_step(
        self,
        context: WorkflowContext,
        step_id: str,
    ) -> None:
        ...