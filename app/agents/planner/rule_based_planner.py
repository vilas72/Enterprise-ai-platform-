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
    Rule-based planner.

    Uses capability mappings to determine the execution plan.
    """

    _DEVELOPER = {
        "search_repository",
        "analyze_repository",
        "repository_health",
        "code_quality",
        "review_pull_request",
        "merge_pull_request",
        "create_github_issue",
        "create_jira_bug",
        "create_jira_story",
        "transition_jira_issue",
        "generate_unit_tests",
        "generate_documentation",
        "architecture_recommendations",
        "explain_code",
    }

    _KNOWLEDGE = {
        "search",
        "answer",
        "summarize",
        "recommend",
        "rewrite",
        "explain",
    }

    _SUPPORT = {
        "search_tickets",
        "create_ticket",
        "update_ticket",
        "transition_ticket",
        "search_knowledge",
        "recommend_articles",
        "similar_incidents",
        "summarize_incident",
        "generate_resolution",
        "escalation_recommendation",
    }

    _DEVOPS = {
        "repository_analysis",
        "repository_health",
        "release_readiness",
        "deployment_analysis",
        "incident_analysis",
        "pull_request_review",
        "code_quality",
    }

    async def plan(
        self,
        request: Any,
    ) -> PlannerResult:

        capability = request.capability

        logger.info(
            "Planning capability '%s'.",
            capability,
        )

        if capability in self._DEVELOPER:
            agent = "developer"

        elif capability in self._KNOWLEDGE:
            agent = "knowledge"

        elif capability in self._SUPPORT:
            agent = "support"

        elif capability in self._DEVOPS:
            agent = "devops"

        else:
            raise ValueError(
                f"Unsupported capability: {capability}"
            )

        return PlannerResult(
            planner="rule_based",
            selected_agent=agent,
            capability=capability,
            confidence=1.0,
            reasoning=f"Capability '{capability}' mapped to '{agent}'.",
            workflow=[
                PlannerStep(
                    order=1,
                    agent=agent,
                    capability=capability,
                    payload=request.payload,
                )
            ],
        )