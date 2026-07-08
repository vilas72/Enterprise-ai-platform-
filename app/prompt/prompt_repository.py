from abc import ABC, abstractmethod

from app.prompt.prompt import Prompt


class PromptRepository(ABC):
    """
    Abstract repository for loading prompt templates.
    """

    @abstractmethod
    def get(
        self,
        name: str,
    ) -> Prompt:
        """
        Load a prompt by name.

        Raises:
            FileNotFoundError
                if the prompt does not exist.
        """
        pass

    @abstractmethod
    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a prompt exists.
        """
        pass

    @abstractmethod
    def list(
        self,
    ) -> list[str]:
        """
        Return all available prompt names.
        """
        pass