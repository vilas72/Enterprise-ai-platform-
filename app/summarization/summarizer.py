"""Conversation summarization for memory management."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.models.chat_message import ChatMessage


class Summarizer(ABC):
    """Abstract summarizer for conversation history."""

    @abstractmethod
    async def summarize(self, messages: list[ChatMessage]) -> str:
        """
        Summarize a list of messages into a concise summary.

        Args:
            messages: List of conversation messages

        Returns:
            Summary string
        """
        raise NotImplementedError


class LLMSummarizer(Summarizer):
    """Summarizer using LLM for high-quality summaries."""

    def __init__(self, ai_service) -> None:
        self.ai_service = ai_service

    async def summarize(self, messages: list[ChatMessage]) -> str:
        """Summarize messages using LLM."""
        if not messages:
            return ""

        # Build conversation text
        conversation_text = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in messages]
        )

        prompt = f"""Summarize the following conversation concisely in 2-3 sentences.
Focus on key decisions, questions asked, and conclusions.

Conversation:
{conversation_text}

Summary:"""

        # TODO: Call AI service to generate summary
        # This is placeholder pending AIService refactor
        return f"Conversation with {len(messages)} messages"


class TrivialSummarizer(Summarizer):
    """Simple summarizer for testing."""

    async def summarize(self, messages: list[ChatMessage]) -> str:
        """Return basic summary stats."""
        if not messages:
            return "No messages"
        return f"Conversation with {len(messages)} messages"
