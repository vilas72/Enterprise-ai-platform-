"""
Application Deployment Workflow Template.
"""

from __future__ import annotations

from enum import StrEnum
from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType


class DeployApplicationTemplate(WorkflowTemplate):
    """
    Workflow template for deploying an application.

    Workflow:

        Validate Deployment Request
                    ↓
            Build Application
                    ↓
             Run Unit Tests
                    ↓
            Build Container Image
                    ↓
              Push Image
                    ↓
           Deploy Application
                    ↓
            Verify Deployment
                    ↓
             Run Smoke Tests
                    ↓
            Notify Deployment
    """

    def __init__(self) -> None:
        super().__init__(
            capability="deploy_application",
            name="Deploy Application",
            description="Build, deploy and verify an enterprise application.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                    id="validate_request",
                    name="Validate Deployment Request",
                    agent="devops",
                    capability="validate_request",
                    action=ActionType.VALIDATE_REQUEST,
                ),
                WorkflowStep(
                    id="build_application",
                    name="Build Application",
                    agent="devops",
                    capability="build_application",
                    action=ActionType.BUILD_APPLICATION,
                    depends_on=["validate_request"],
                ),
                WorkflowStep(
                    id="run_unit_tests",
                    name="Run Unit Tests",
                    agent="devops",
                    capability="run_unit_tests",
                    action=ActionType.RUN_UNIT_TESTS,
                    depends_on=["build_application"],
                ),
                WorkflowStep(
                    id="build_container",
                    name="Build Container Image",
                    agent="devops",
                    capability="build_container",
                    action=ActionType.BUILD_CONTAINER,
                    depends_on=["run_unit_tests"],
                ),
                WorkflowStep(
                    id="push_container",
                    name="Push Container Image",
                    agent="devops",
                    capability="push_container",
                    action=ActionType.PUSH_CONTAINER,
                    depends_on=["build_container"],
                ),
                WorkflowStep(
                    id="deploy_application",
                    name="Deploy Application",
                    agent="devops",
                    capability="deploy_application",
                    action=ActionType.DEPLOY_APPLICATION,
                    depends_on=["push_container"],
                ),
                WorkflowStep(
                    id="verify_deployment",
                    name="Verify Deployment",
                    agent="devops",
                    capability="verify_deployment",
                    action=ActionType.VERIFY_DEPLOYMENT,
                    depends_on=["deploy_application"],
                ),
                WorkflowStep(
                    id="run_smoke_tests",
                    name="Run Smoke Tests",
                    agent="devops",
                    capability="run_smoke_tests",
                    action=ActionType.RUN_SMOKE_TESTS,
                    depends_on=["verify_deployment"],
                ),
                WorkflowStep(
                    id="notify_team",
                    name="Notify Team",
                    agent="devops",
                    capability="notify_team",
                    action=ActionType.NOTIFY_TEAM,
                    depends_on=["run_smoke_tests"],
                ),
            ],
        )
   