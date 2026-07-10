from __future__ import annotations

import logging
from typing import Protocol

from app.rag.rag_request import RagRequest

logger = logging.getLogger(__name__)


class QueryRewriteClient(Protocol):
    """Contract for any AI service capable of rewriting queries."""

    async def rewrite_query(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> str:
        ...


class QueryRewriter:
    """Rewrites conversational follow-up questions into standalone search queries."""

    def __init__(
        self,
        client: QueryRewriteClient,
    ) -> None:
        self._client = client

    async def rewrite(
        self,
        request: RagRequest,
    ) -> str:
        """Rewrite the user's query into a standalone search query."""

        if not request.enable_query_rewrite:
            return request.query

        try:
            rewritten = await self._client.rewrite_query(
                system_prompt=self._system_prompt(),
                user_prompt=self._build_prompt(request),
                temperature=0.0,
            )
            rewritten = rewritten.strip()

            if rewritten:
                logger.debug(
                    "Query rewritten: '%s' -> '%s'",
                    request.query,
                    rewritten,
                )
                return rewritten
        except Exception:
            logger.exception("Failed to rewrite query.")

        return request.query

    def _build_prompt(
        self,
        request: RagRequest,
    ) -> str:
        history = "\n".join(request.recent_messages)
        memories = "\n".join(request.semantic_memories)
        summary = request.conversation_summary or ""

        return f"""
Conversation Summary:
{summary}

Recent Conversation:
{history}

Relevant Memories:
{memories}

Current User Question:
{request.query}

Rewrite the current question into a standalone search query.

Rules:
- Preserve the original intent.
- Resolve references like "it", "that", "they", and "this".
- Do NOT answer the question.
- Return ONLY the rewritten query.
- If rewriting is unnecessary, return the original question.
"""

    @staticmethod
    def _system_prompt() -> str:
        return (
            "You are an enterprise retrieval query rewriting assistant. "
            "Rewrite conversational follow-up questions into standalone "
            "search queries without answering them."
        )
