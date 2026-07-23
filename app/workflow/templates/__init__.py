"""
Workflow Template Registration.
"""

from app.workflow.templates.workflow_template_registry import (
    WorkflowTemplateRegistry,
)

from app.workflow.templates.developer.review_pull_request import (
    ReviewPullRequestTemplate,
)
from app.workflow.templates.support.search_tickets import (
    SearchTicketsTemplate,
)

from app.workflow.templates.support.update_ticket import (
    UpdateTicketTemplate,
)
from app.workflow.templates.support.create_ticket import (
    CreateTicketTemplate,
)

from app.workflow.templates.knowledge.search_repository import (
    SearchRepositoryTemplate,
)

from app.workflow.templates.support.resolve_ticket import (
    ResolveTicketTemplate,
)

from app.workflow.templates.devops.deploy_application import (
    DeployApplicationTemplate,
)


def register_workflow_templates(
    registry: WorkflowTemplateRegistry,
) -> None:
    """
    Register all workflow templates.
    """

    registry.register(
        ReviewPullRequestTemplate(),
    )

    registry.register(
        SearchRepositoryTemplate(),
    )

    registry.register(
        ResolveTicketTemplate(),
    )

    registry.register(
        DeployApplicationTemplate(),
    )

    registry.register(
        CreateTicketTemplate(),
    )

    registry.register(
        UpdateTicketTemplate(),
    )

    registry.register(
        SearchTicketsTemplate(),
    )