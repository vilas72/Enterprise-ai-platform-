"""
Enterprise Gateway Router.
"""

from __future__ import annotations

import logging
from typing import Any

from app.agents.developer.models import DeveloperAgentRequest, DeveloperCapability, JiraIssueReference, PullRequestReference, RepositoryReference
from app.agents.devops.models import DevOpsAgentRequest, DevOpsCapability
from app.agents.knowledge.models import KnowledgeAgentRequest, KnowledgeCapability
from app.agents.support.models import SupportAgentRequest, SupportCapability

from app.agents.developer.developer_agent import DeveloperAgent
from app.agents.knowledge.knowledge_agent import KnowledgeAgent
from app.agents.support.support_agent import SupportAgent
from app.agents.devops.devops_agent import DevOpsAgent



from app.gateway.exceptions import (
    UnsupportedCapabilityError,
)
from app.gateway.models import (
    GatewayRequest,
)
from app.gateway.registry import (
    GatewayRegistry,
)

logger = logging.getLogger(__name__)


class GatewayRouter:
    """
    Responsible for selecting the appropriate
    business agent.
    """

    def __init__(
        self,
        registry: GatewayRegistry,
    ) -> None:

        self._registry = registry

    def get_agent(
        self,
        agent_name: str,
    ) -> Any:
        """
        Return a registered agent by name.
        """

        logger.info(
            "Resolving agent '%s'.",
            agent_name,
        )

        try:
            return self._registry.get(agent_name)

        except Exception as exc:
            raise UnsupportedCapabilityError(
                f"Unknown agent '{agent_name}'."
            ) from exc
            
    async def route(
        self,
        request: GatewayRequest,
    ) -> Any:
        """
        Resolve an agent for the request.
        """

        logger.info(
            "Routing capability '%s'.",
            request.capability,
        )

        try:

            return self._registry.find_by_capability(
                request.capability,
            )

        except Exception as exc:

            raise UnsupportedCapabilityError(
                f"No agent found for "
                f"'{request.capability}'."
            ) from exc

    def registered_agents(
        self,
    ) -> list[str]:
        """
        List registered agents.
        """

        return self._registry.names()

    def supported_capabilities(
        self,
    ) -> dict[str, list[str]]:
        """
        Return all supported capabilities.
        """

        return self._registry.supported_capabilities()
    
    def build_agent_request(
        self,
        *,
        agent: Any,
        capability: str,
        request: GatewayRequest,
    ) -> Any:
        """
        Build an agent-specific request from the GatewayRequest.
        """

        payload = request.payload or {}
        
        repo_payload = payload.get("repository")

        pr_payload = payload.get("pull_request")

        repository = None
        pull_request = None
        jira_issue = None 
        
        issue_payload = payload.get("jira_issue")
        

        if isinstance(repo_payload, dict):
            repository = RepositoryReference(
                owner=repo_payload["owner"],
                repository=repo_payload["repository"],
                branch=repo_payload.get("branch"),
            )
            
        if isinstance(pr_payload, dict):
                pr_repo = pr_payload.get("repository", {})
                
                pull_request = PullRequestReference(
                pull_request_number=pr_payload["pull_request_number"],
                repository=RepositoryReference(
                    owner=pr_repo["owner"],
                    repository=pr_repo["repository"],
                    branch=pr_repo.get("branch"),
                ),
            ) 
                
        if isinstance(issue_payload, dict):
            jira_issue = JiraIssueReference.model_validate(issue_payload)
        elif payload.get("issue_key"):
            jira_issue = JiraIssueReference(
                issue_key=payload["issue_key"]
            )

        if isinstance(agent, DeveloperAgent):
            return DeveloperAgentRequest(
                capability=DeveloperCapability(capability),
                metadata={**request.metadata, **payload},
                query=payload.get("query"),
                title=payload.get("title"),
                description=payload.get("description"),
                repository=repository,
                pull_request=pull_request,
                project_key=payload.get("project_key"),
                jira_issue=jira_issue,
                transition_id=payload.get("transition_id"),
            )

        elif isinstance(agent, KnowledgeAgent):
            return KnowledgeAgentRequest(
                capability=KnowledgeCapability(capability),
                query=payload.get("query") or request.metadata.get("query") or "query",
                source=payload.get("source", "all"),
                top_k=payload.get("top_k", 5),
                filters=payload.get("filters", {}),
                repository=repository,
            )

        elif isinstance(agent, SupportAgent):
            return SupportAgentRequest(
                capability=SupportCapability(capability),
                payload=payload,
                metadata=request.metadata,
                query=payload.get("query"),
                repository=repository,
                ticket_key=payload.get("ticket_key"),
                project_key=payload.get("project_key"),
                title=payload.get("title"),
                description=payload.get("description"),
            )

        elif isinstance(agent, DevOpsAgent):
            return DevOpsAgentRequest(
                capability=DevOpsCapability(capability),
                payload=payload,
                metadata=request.metadata,
                owner=payload.get("owner"),
                repository=repository,
                pull_request=payload.get("pull_request"),
                issue=payload.get("issue"),
                branch=payload.get("branch"),
                release=payload.get("release"),
                deployment=payload.get("deployment"),
                query=payload.get("query"),
            )

        raise TypeError(
            f"Unsupported agent type: {type(agent).__name__}"
        )
    
    def get_registered_agent(
        self,
        name: str,
    ) -> Any:
        """
        Convenience wrapper.
        """

        return self.get_agent(name)