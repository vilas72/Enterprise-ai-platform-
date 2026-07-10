"""Unit tests for conversation service."""

import pytest
from app.conversation.conversation_service import ConversationService, ConversationNotFoundError
from app.conversation.in_memory_store import InMemoryConversationStore
from app.conversation.conversation_message import MessageRole


@pytest.mark.asyncio
async def test_create_conversation():
    """Test creating a new conversation."""
    store = InMemoryConversationStore()
    service = ConversationService(conversation_store=store)

    conversation = await service.create_conversation(
        conversation_id="conv-123", title="Test Conversation"
    )

    assert conversation.conversation_id == "conv-123"
    assert conversation.title == "Test Conversation"
    assert len(conversation.messages) == 0


@pytest.mark.asyncio
async def test_get_conversation():
    """Test retrieving a conversation."""
    store = InMemoryConversationStore()
    service = ConversationService(conversation_store=store)

    # Create a conversation
    created = await service.create_conversation(conversation_id="conv-123")

    # Retrieve it
    retrieved = await service.get_conversation("conv-123")

    assert retrieved is not None
    assert retrieved.conversation_id == created.conversation_id


@pytest.mark.asyncio
async def test_add_message():
    """Test adding a message to a conversation."""
    store = InMemoryConversationStore()
    service = ConversationService(conversation_store=store)

    # Create conversation and add message
    conversation = await service.create_conversation(conversation_id="conv-123")

    message = await service.add_message(
        "conv-123",
        role=MessageRole.USER,
        content="Hello, how are you?",
    )

    assert message.role == MessageRole.USER
    assert message.content == "Hello, how are you?"

    # Verify message was added
    messages = await service.get_messages("conv-123")
    assert len(messages) == 1
    assert messages[0].content == "Hello, how are you?"


@pytest.mark.asyncio
async def test_conversation_not_found():
    """Test retrieving non-existent conversation raises error."""
    store = InMemoryConversationStore()
    service = ConversationService(conversation_store=store)

    with pytest.raises(ConversationNotFoundError):
        await service.get_conversation("non-existent")


@pytest.mark.asyncio
async def test_delete_conversation():
    """Test deleting a conversation."""
    store = InMemoryConversationStore()
    service = ConversationService(conversation_store=store)

    # Create and delete
    await service.create_conversation(conversation_id="conv-123")
    await service.delete_conversation("conv-123")

    # Verify it's gone
    with pytest.raises(ConversationNotFoundError):
        await service.get_conversation("conv-123")
