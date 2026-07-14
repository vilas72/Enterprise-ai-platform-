"""
Planner prompt builder.
"""

from __future__ import annotations

from app.agents.models.agent_request import AgentRequest


class PlannerPrompt:
    """
    Builds prompts for LLM planning.
    """

    @staticmethod
    def build(
        request: AgentRequest,
    ) -> str:

        return f"""
You are an Enterprise AI Planner.

Do NOT answer the user.

Create an execution plan.

Available actions

- reason
- retrieve
- tools
- generate

Return JSON only.

Task

{request.task}

Query

{request.query}

Memory Enabled

{request.enable_memory}

Knowledge Retrieval

{request.enable_rag}

Tool Execution

{request.enable_tools}
"""