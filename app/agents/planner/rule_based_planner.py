"""
Enterprise Rule-Based Planner.

Provides deterministic planning without requiring an LLM.
"""

from __future__ import annotations

import logging
from typing import Any

from app.agents.planner.planner import Planner
from app.agents.planner.planner_result import (
    PlannerResult,
    PlannerStep,
)

logger = logging.getLogger(__name__)


class RuleBasedPlanner(Planner):
    """
    Enterprise rule-based planner.

    Maps business capabilities to the appropriate workflow and agent.
    """

    _CAPABILITY_MAP = {

        #
        # Developer Workflow
        #
        "review_pull_request": ("developer", "review_pull_request"),
        "merge_pull_request": ("developer", "review_pull_request"),
        "search_repository": ("developer", "review_pull_request"),
        "analyze_repository": ("developer", "review_pull_request"),
        "repository_health": ("developer", "review_pull_request"),
        "create_github_issue": ("developer", "review_pull_request"),
        "create_jira_bug": ("developer", "review_pull_request"),
        "create_jira_story": ("developer", "review_pull_request"),
        "transition_jira_issue": ("developer", "review_pull_request"),
        "generate_unit_tests": ("developer", "review_pull_request"),
        "generate_documentation": ("developer", "review_pull_request"),
        "architecture_recommendations": ("developer", "review_pull_request"),
        "explain_code": ("developer", "review_pull_request"),

        #
        # Knowledge Workflow
        #
        "search": ("knowledge", "search_repository"),
        "answer": ("knowledge", "search_repository"),
        "summarize": ("knowledge", "search_repository"),
        "recommend": ("knowledge", "search_repository"),
        "rewrite": ("knowledge", "search_repository"),
        "explain": ("knowledge", "search_repository"),

        #
        # Support Workflow
        #
        "create_ticket": ("support", "create_ticket"),
        "search_tickets": ("support", "search_tickets"),
        "update_ticket": ("support", "update_ticket"),
        "transition_ticket": ("support", "transition_ticket"),
        "resolve_ticket": ("support", "resolve_ticket"),
        "search_knowledge": ("support", "search_knowledge"),
        "recommend_articles": ("support", "recommend_articles"),
        "similar_incidents": ("support", "similar_incidents"),
        "summarize_incident": ("support", "summarize_incident"),
        "generate_resolution": ("support", "generate_resolution"),
        "escalation_recommendation": ("support", "escalation_recommendation"),

        #
        # DevOps Workflow
        #
        "deploy_application": ("devops", "deploy_application"),
        "repository_analysis": ("devops", "deploy_application"),
        "release_readiness": ("devops", "deploy_application"),
        "deployment_analysis": ("devops", "deploy_application"),
        "incident_analysis": ("devops", "deploy_application"),
        "pull_request_review": ("devops", "deploy_application"),
        "code_quality": ("devops", "deploy_application"),
    }

    async def plan(
        self,
        request: Any,
    ) -> PlannerResult:
        """
        Build a deterministic execution plan.
        """

        requested_capability = request.capability

        logger.info(
            "Planning capability '%s'.",
            requested_capability,
        )

        try:
            agent, workflow_capability = self._CAPABILITY_MAP[
                requested_capability
            ]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported capability: {requested_capability}"
            ) from exc

        return PlannerResult(
            planner="rule_based",
            selected_agent=agent,
            requested_capability=requested_capability,
            workflow_capability=workflow_capability,
            payload=request.payload,
            workflow=[
                PlannerStep(
                    order=1,
                    agent=agent,
                    capability=workflow_capability,
                    payload=request.payload,
                )
            ],
        )