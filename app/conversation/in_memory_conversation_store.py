from __future__ import annotations

from copy import deepcopy

import asyncio

from app.conversation.conversation import Conversation
from app.conversation.conversation_store import ConversationStore


class InMemoryConversationStore(ConversationStore):
    """
    In-memory implementation of the ConversationStore.

    Intended for:
    - Local development
    - Unit testing
    - Integration testing
    - Small deployments

    This implementation is thread-safe for concurrent async access
    within a single application instance.
    """

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._lock = asyncio.Lock()

    async def create(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Persist a new conversation.

        Raises:
            ValueError:
                If the conversation already exists.
        """
        async with self._lock:
            if conversation.conversation_id in self._conversations:
                raise ValueError(
                    f"Conversation '{conversation.conversation_id}' already exists."
                )

            self._conversations[
                conversation.conversation_id
            ] = deepcopy(conversation)

    async def save(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Create or update a conversation.
        """
        async with self._lock:
            self._conversations[
                conversation.conversation_id
            ] = deepcopy(conversation)

    async def get(
        self,
        conversation_id: str,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its identifier.
        """
        async with self._lock:
            conversation = self._conversations.get(conversation_id)

            if conversation is None:
                return None

            return deepcopy(conversation)

    async def delete(
        self,
        conversation_id: str,
    ) -> bool:
        """
        Delete a conversation.
        """
        async with self._lock:
            return (
                self._conversations.pop(conversation_id, None)
                is not None
            )

    async def exists(
        self,
        conversation_id: str,
    ) -> bool:
        """
        Determine whether a conversation exists.
        """
        async with self._lock:
            return conversation_id in self._conversations

    async def list(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Conversation]:
        """
        Return a paginated list of conversations ordered
        by creation time.
        """
        async with self._lock:
            conversations = sorted(
                self._conversations.values(),
                key=lambda conversation: conversation.created_at,
            )

            conversations = conversations[offset : offset + limit]

            return [
                deepcopy(conversation)
                for conversation in conversations
            ]

    async def count(self) -> int:
        """
        Return the total number of conversations.
        """
        async with self._lock:
            return len(self._conversations)

    async def clear(self) -> None:
        """
        Remove all conversations.
        """
        async with self._lock:
            self._conversations.clear()