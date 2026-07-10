"""Integration tests for conversation workflow."""

import pytest
from app.conversation.conversation_service import ConversationService
from app.conversation.in_memory_store import InMemoryConversationStore
from app.conversation.conversation_message import MessageRole
from app.conversation.conversation_memory_manager import ConversationMemoryManager


@pytest.fixture
def conversation_workflow():
    """Create a full conversation workflow for testing."""
    store = InMemoryConversationStore()
    service = ConversationService(conversation_store=store)
    memory_manager = ConversationMemoryManager()
    return service, memory_manager


@pytest.mark.asyncio
async def test_conversation_workflow(conversation_workflow):
    """Test complete conversation workflow."""
    service, memory_manager = conversation_workflow

    # Create conversation
    conv = await service.create_conversation(
        conversation_id="workflow-1", title="Integration Test"
    )

    # Add user message
    msg1 = await service.add_message(
        "workflow-1", role=MessageRole.USER, content="What is AI?"
    )
    assert msg1 is not None

    # Add assistant response
    msg2 = await service.add_message(
        "workflow-1", role=MessageRole.ASSISTANT, content="AI is artificial intelligence"
    )
    assert msg2 is not None

    # Retrieve conversation
    messages = await service.get_messages("workflow-1")
    assert len(messages) == 2

    # Apply memory policy
    retrieved_conv = await service.get_conversation("workflow-1")
    memory_manager.apply(retrieved_conv)

    # Verify conversation still intact
    messages = await service.get_messages("workflow-1")
    assert len(messages) >= 1


@pytest.mark.asyncio
async def test_multi_turn_conversation(conversation_workflow):
    """Test multi-turn conversation."""
    service, _ = conversation_workflow

    conv_id = "multi-turn-1"
    await service.create_conversation(conversation_id=conv_id)

    # Multiple turns
    turns = [
        (MessageRole.USER, "Hello"),
        (MessageRole.ASSISTANT, "Hi there!"),
        (MessageRole.USER, "How are you?"),
        (MessageRole.ASSISTANT, "I'm doing well, thank you!"),
    ]

    for role, content in turns:
        await service.add_message(conv_id, role=role, content=content)

    messages = await service.get_messages(conv_id)
    assert len(messages) == len(turns)


@pytest.mark.asyncio
async def test_conversation_rename(conversation_workflow):
    """Test renaming a conversation."""
    service, _ = conversation_workflow

    conv = await service.create_conversation(
        conversation_id="rename-1", title="Original"
    )

    renamed = await service.rename_conversation("rename-1", "Updated Title")

    assert renamed.title == "Updated Title"
