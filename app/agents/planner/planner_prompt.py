"""
Planner prompt builder.
"""

from __future__ import annotations

from app.agents.models.agent_request import AgentRequest


class PlannerPrompt:
    """
    Builds prompts for the LLM Planner.

    The planner is responsible for deciding
    which execution steps are required to
    satisfy a user request.
    """

    @staticmethod
    def build(
        request: AgentRequest,
    ) -> str:

        return f"""
You are an Enterprise AI Agent Planner.

Your task is NOT to answer the user.

Your task is ONLY to create an execution plan.

Available actions:

- reason
- retrieve
- tools
- generate

Return ONLY valid JSON.

Example:

{{
  "reasoning": "...",
  "confidence": 0.95,
  "steps": [
    {{
      "name":"Reason",
      "description":"Understand the task",
      "action":"reason"
    }},
    {{
      "name":"Retrieve",
      "description":"Retrieve enterprise knowledge",
      "action":"retrieve"
    }},
    {{
      "name":"Generate",
      "description":"Generate final response",
      "action":"generate"
    }}
  ]
}}

Task

{request.task}

User Query

{request.query}
"""