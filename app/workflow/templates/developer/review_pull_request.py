"""
Review Pull Request Workflow Template.
"""

from __future__ import annotations

from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class ReviewPullRequestTemplate(WorkflowTemplate):
    """
    Workflow template for reviewing a GitHub Pull Request.

    Workflow:

        Fetch Pull Request
                ↓
        Fetch Changed Files
                ↓
        Analyze Code
                ↓
        Generate Review
                ↓
        Publish Review
    """

    def __init__(self) -> None:
        super().__init__(
            capability="review_pull_request",
            name="Review Pull Request",
            description="Analyze a GitHub Pull Request and generate an AI review.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                    id="fetch_pr",
                    name="Fetch Pull Request",
                    agent="developer",
                    capability="review_pull_request",
                    action=ActionType.FETCH_PULL_REQUEST,
                ),
                WorkflowStep(
                    id="fetch_files",
                    name="Fetch Changed Files",
                    agent="developer",
                    capability="review_pull_request",
                    action=ActionType.FETCH_CHANGED_FILES,
                    depends_on=["fetch_pr"],
                ),
                WorkflowStep(
                    id="analyze_code",
                    name="Analyze Source Code",
                    agent="developer",
                    capability="review_pull_request",
                    action=ActionType.ANALYZE_CODE,
                    depends_on=["fetch_files"],
                ),
                WorkflowStep(
                    id="generate_review",
                    name="Generate AI Review",
                    agent="developer",
                    capability="review_pull_request",
                    action=ActionType.GENERATE_REVIEW,
                    depends_on=["analyze_code"],
                ),
                WorkflowStep(
                    id="publish_review",
                    name="Publish Review",
                    agent="developer",
                    capability="review_pull_request",
                    action=ActionType.PUBLISH_REVIEW,
                    depends_on=["generate_review"],
                ),
            ],
        )

