from app.agents.developer.models import DeveloperAgentRequest, DeveloperCapability
from app.agents.devops.models import DevOpsCapability
from app.agents.devops.models import DevOpsAgentRequest
from app.agents.knowledge.models import KnowledgeAgentRequest
from app.agents.support.models import SupportAgentRequest
from app.gateway.models import GatewayRequest

from app.agents.developer.models import (
    DeveloperAgentRequest,
    DeveloperCapability,
    RepositoryReference,
    PullRequestReference,
    JiraIssueReference,
)

from app.agents.support.models import (
    SupportAgentRequest,
    SupportCapability,
)


class AgentRequestFactory:

    def create(
        self,
        agent_name: str,
        capability: str,
        request: GatewayRequest,
    ):
        payload = request.payload or {}
        
        if agent_name == "developer":
            repository = None
            if isinstance(payload.get("repository"), dict):
                repository = RepositoryReference.model_validate(
                    payload["repository"]
                )

            pull_request = None
            if isinstance(payload.get("pull_request"), dict):
                pull_request = PullRequestReference.model_validate(
                    payload["pull_request"]
                )

            jira_issue = None
            if isinstance(payload.get("jira_issue"), dict):
                jira_issue = JiraIssueReference.model_validate(
                    payload["jira_issue"]
                )

            return DeveloperAgentRequest(
                capability=DeveloperCapability(capability),
                conversation_id=request.request_id,
                repository=repository,
                pull_request=pull_request,
                jira_issue=jira_issue,
                query=payload.get("query"),
                code=payload.get("code"),
                path=payload.get("path"),
                title=payload.get("title"),
                description=payload.get("description"),
                project_key=payload.get("project_key"),
                transition_id=payload.get("transition_id"),
                metadata=request.metadata,
            )

        if agent_name == "devops":
            return DevOpsAgentRequest( 
                capability=DevOpsCapability(capability),
                conversation_id=request.request_id,
                query=payload.get("query"),
                code=payload.get("code"),
                title=payload.get("title"),
                description=payload.get("description"),
                metadata=request.metadata,
            )

        if agent_name == "knowledge":
            return KnowledgeAgentRequest( 
                capability=capability,
                conversation_id=request.request_id,
                query=payload.get("query"),
                code=payload.get("code"),
                title=payload.get("title"),
                description=payload.get("description"),
                metadata=request.metadata,
            )
        
        if agent_name == "support":
             return SupportAgentRequest(
                capability=SupportCapability(capability),

                conversation_id=request.request_id,
                query=payload.get("query"),
                ticket_key=payload.get("ticket_key"),
                project_key=payload.get("project_key"),

                title=payload.get("title"),
                description=payload.get("description"),

                status=payload.get("status"),
                assignee=payload.get("assignee"),
                max_results=payload.get("max_results"),

                payload=payload,
                metadata=request.metadata,
            )

        raise ValueError(f"Unsupported agent: {agent_name}")