"""Unit tests for summarization module."""

import pytest
from app.summarization.summarizer import TrivialSummarizer, LLMSummarizer
from app.domain.models.chat_message import ChatMessage


@pytest.mark.asyncio
async def test_trivial_summarizer():
    """Test basic summarizer."""
    summarizer = TrivialSummarizer()

    messages = [
        ChatMessage(conversation_id="conv-1", role="user", content="Hello"),
        ChatMessage(conversation_id="conv-1", role="assistant", content="Hi there"),
    ]

    summary = await summarizer.summarize(messages)

    assert "2" in summary or "messages" in summary


@pytest.mark.asyncio
async def test_trivial_summarizer_empty():
    """Test summarizer with no messages."""
    summarizer = TrivialSummarizer()

    summary = await summarizer.summarize([])

    assert summary == "No messages"


@pytest.mark.asyncio
async def test_llm_summarizer():
    """Test LLM-based summarizer."""
    from tests.mocks.mock_services import MockAIService

    ai_service = MockAIService()
    summarizer = LLMSummarizer(ai_service=ai_service)

    messages = [
        ChatMessage(conversation_id="conv-1", role="user", content="What is AI?"),
        ChatMessage(
            conversation_id="conv-1",
            role="assistant",
            content="AI is artificial intelligence",
        ),
    ]

    summary = await summarizer.summarize(messages)

    assert len(summary) > 0
