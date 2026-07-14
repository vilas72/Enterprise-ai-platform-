"""Agent memory service."""

from __future__ import annotations

from typing import Any

from app.agents.models.agent_memory import AgentMemory


class AgentMemoryService:
    """
    Service for managing agent memory state and history.

    Handles short-term and long-term memory operations.
    """

    def __init__(self):
        """Initialize the agent memory service."""
        self._memories: dict[str, AgentMemory] = {}

    def create_memory(self, memory_id: str) -> AgentMemory:
        """
        Create a new memory instance.

        Args:
            memory_id: Unique identifier for the memory

        Returns:
            Newly created AgentMemory instance
        """
        memory = AgentMemory(memory_id=memory_id)
        self._memories[memory_id] = memory
        return memory

    def get_memory(self, memory_id: str) -> AgentMemory:
        """
        Retrieve memory by ID.

        Args:
            memory_id: The memory identifier

        Returns:
            The AgentMemory instance

        Raises:
            KeyError: If memory not found
        """
        if memory_id not in self._memories:
            raise KeyError(f"Memory {memory_id} not found")
        return self._memories[memory_id]

    def add_short_term(self, memory_id: str, key: str, value: Any) -> None:
        """
        Add to short-term memory.

        Args:
            memory_id: The memory identifier
            key: Memory key
            value: Memory value
        """
        memory = self.get_memory(memory_id)
        memory.short_term[key] = value

    def add_long_term(self, memory_id: str, key: str, value: Any) -> None:
        """
        Add to long-term memory.

        Args:
            memory_id: The memory identifier
            key: Memory key
            value: Memory value
        """
        memory = self.get_memory(memory_id)
        memory.long_term[key] = value

    def add_observation(self, memory_id: str, observation: str) -> None:
        """
        Add an observation to memory.

        Args:
            memory_id: The memory identifier
            observation: The observation to record
        """
        memory = self.get_memory(memory_id)
        memory.observations.append(observation)

    def add_insight(self, memory_id: str, insight: str) -> None:
        """
        Add an insight to memory.

        Args:
            memory_id: The memory identifier
            insight: The insight to record
        """
        memory = self.get_memory(memory_id)
        memory.insights.append(insight)

    def clear_short_term(self, memory_id: str) -> None:
        """
        Clear short-term memory.

        Args:
            memory_id: The memory identifier
        """
        memory = self.get_memory(memory_id)
        memory.short_term.clear()

    def delete_memory(self, memory_id: str) -> None:
        """
        Delete a memory instance.

        Args:
            memory_id: The memory identifier

        Raises:
            KeyError: If memory not found
        """
        if memory_id not in self._memories:
            raise KeyError(f"Memory {memory_id} not found")
        del self._memories[memory_id]
