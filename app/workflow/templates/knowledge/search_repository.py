"""
Repository Search Workflow Template.
"""

from __future__ import annotations
from enum import StrEnum

from app.workflow.models.workflow_step import WorkflowStep
from app.workflow.templates.workflow_template import WorkflowTemplate
from app.workflow.models.action_type import ActionType

class SearchRepositoryTemplate(WorkflowTemplate):
    """
    Workflow template for enterprise knowledge retrieval.

    Workflow:

        Hybrid Search
              ↓
        Rerank Results
              ↓
        Build Context
              ↓
        Generate Answer
    """

    def __init__(self) -> None:
        super().__init__(
            capability="search_repository",
            name="Repository Search",
            description="Search enterprise knowledge and generate an AI response.",
            version="1.0.0",
            steps=[
                WorkflowStep(
                    id="hybrid_search",
                    name="Hybrid Search",
                    agent="knowledge",
                    description="Perform a hybrid search across the repository.",
                    capability="search_repository",
                    action=ActionType.HYBRID_SEARCH,
                ),
                WorkflowStep(
                    id="rerank_results",
                    name="Rerank Search Results",
                    agent="knowledge",
                    description="Rerank the search results based on relevance.",
                    capability="search_repository",
                    action=ActionType.RERANK_RESULTS,
                    depends_on=["hybrid_search"],
                ),
                WorkflowStep(
                    id="build_context",
                    name="Build Retrieval Context",
                    agent="knowledge",
                    description="Build the context for retrieval based on the reranked results.",
                    capability="search_repository",
                    action=ActionType.BUILD_CONTEXT,
                    depends_on=["rerank_results"],
                ),
                WorkflowStep(
                    id="generate_answer",
                    name="Generate AI Response",
                    agent="knowledge",
                    description="Generate an AI response based on the built context.",
                    capability="search_repository",
                    action=ActionType.GENERATE_ANSWER,
                    depends_on=["build_context"],
                ),
            ],
        )
