from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.conversation.conversation import Conversation
from app.conversation.conversation_message import (
    ConversationMessage,
    MessageRole,
)
from app.conversation.conversation_store import ConversationStore


class ConversationNotFoundError(Exception):
    """
    Raised when a conversation cannot be found.
    """


class ConversationService:
    """
    Application service responsible for managing conversations.

    Responsibilities:
    - Create conversations
    - Retrieve conversations
    - Persist conversations
    - Manage conversation messages
    - Delegate persistence to ConversationStore

    This service contains conversation business operations and
    remains independent of AI providers, HTTP, RAG, Memory,
    Agents, and Workflow orchestration.
    """

    def __init__(
        self,
        conversation_store: ConversationStore,
    ) -> None:
        self._conversation_store = conversation_store

    async def create_conversation(
        self,
        *,
        conversation_id: str | None = None,
        title: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> Conversation:
        """
        Create and persist a new conversation.
        """

        if conversation_id is not None:
            conversation_id = conversation_id.strip()

            if not conversation_id:
                raise ValueError(
                    "conversation_id cannot be empty."
                )

        conversation = Conversation(
            conversation_id=conversation_id,
            title=title,
            metadata=dict(metadata or {}),
        )

        await self._conversation_store.create(
            conversation
        )

        return conversation

    async def get_or_create_conversation(
        self,
        conversation_id: str,
    ) -> Conversation:
        """
        Retrieve an existing conversation or create one if it
        does not already exist.
        """

        conversation_id = conversation_id.strip()

        if not conversation_id:
            raise ValueError(
                "conversation_id cannot be empty."
            )

        conversation = await self._conversation_store.get(
            conversation_id
        )

        if conversation is not None:
            return conversation

        return await self.create_conversation(
            conversation_id=conversation_id,
        )

    async def get_conversation(
        self,
        conversation_id: str,
    ) -> Conversation:
        """
        Retrieve a conversation.

        Raises:
            ConversationNotFoundError
        """

        conversation_id = conversation_id.strip()

        if not conversation_id:
            raise ValueError(
                "conversation_id cannot be empty."
            )

        conversation = await self._conversation_store.get(
            conversation_id
        )

        if conversation is None:
            raise ConversationNotFoundError(
                f"Conversation '{conversation_id}' not found."
            )

        return conversation

    async def save(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Persist a conversation.

        This method should be used by future components such as:
        - MemoryManager
        - RAG
        - Agent Framework
        - Workflow Engine
        """

        await self._conversation_store.save(
            conversation
        )

    async def delete_conversation(
        self,
        conversation_id: str,
    ) -> None:
        """
        Delete a conversation.
        """

        conversation_id = conversation_id.strip()

        if not conversation_id:
            raise ValueError(
                "conversation_id cannot be empty."
            )

        deleted = await self._conversation_store.delete(
            conversation_id
        )

        if not deleted:
            raise ConversationNotFoundError(
                f"Conversation '{conversation_id}' not found."
            )

    async def rename_conversation(
        self,
        conversation_id: str,
        title: str,
    ) -> Conversation:
        """
        Rename an existing conversation.
        """

        title = title.strip()

        if not title:
            raise ValueError(
                "title cannot be empty."
            )

        conversation = await self.get_conversation(
            conversation_id
        )

        conversation.rename(title)

        await self.save(conversation)

        return conversation

    async def add_message(
        self,
        conversation_id: str,
        *,
        role: MessageRole,
        content: str,
        metadata: Mapping[str, Any] | None = None,
        token_count: int | None = None,
        model: str | None = None,
    ) -> ConversationMessage:
        """
        Add a message to a conversation.

        If the conversation does not exist,
        it will be created automatically.
        """

        if not content.strip():
            raise ValueError(
                "content cannot be empty."
            )

        conversation = await self.get_or_create_conversation(
            conversation_id
        )

        message = conversation.add_message(
            role=role,
            content=content,
            metadata=dict(metadata or {}),
            token_count=token_count,
            model=model,
        )

        await self.save(conversation)

        return message

    async def get_messages(
        self,
        conversation_id: str,
    ) -> list[ConversationMessage]:
        """
        Return all messages for a conversation.
        """

        conversation = await self.get_conversation(
            conversation_id
        )

        return conversation.get_messages()

    async def list_conversations(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Conversation]:
        """
        Return a paginated list of conversations.
        """

        return await self._conversation_store.list(
            limit=limit,
            offset=offset,
        )

    async def conversation_exists(
        self,
        conversation_id: str,
    ) -> bool:
        """
        Check whether a conversation exists.
        """

        conversation_id = conversation_id.strip()

        if not conversation_id:
            return False

        return await self._conversation_store.exists(
            conversation_id
        )

    async def clear_conversations(self) -> None:
        """
        Remove all conversations.

        Intended primarily for testing and
        development environments.
        """

        await self._conversation_store.clear()

    async def conversation_count(self) -> int:
        """
        Return the total number of conversations.
        """

        return await self._conversation_store.count()