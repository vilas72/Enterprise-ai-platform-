from pathlib import Path

from app.prompt.prompt import Prompt
from app.prompt.prompt_repository import PromptRepository


class FilePromptRepository(PromptRepository):
    """
    Loads prompts from the filesystem.

    Example:

        app/prompts/system_prompt.txt
        app/prompts/assistant_prompt.txt
    """

    def __init__(
        self,
        prompt_directory: str = "app/prompts",
    ) -> None:

        self._prompt_directory = Path(prompt_directory)

    def get(
        self,
        name: str,
    ) -> Prompt:
        """
        Load a prompt by name.
        """

        file_path = self._prompt_directory / f"{name}.txt"
        print(file_path)
        if not file_path.exists():
            raise FileNotFoundError(
                f"Prompt '{name}' not found."
            )

        content = file_path.read_text(
            encoding="utf-8"
        )

        return Prompt(
            name=name,
            content=content,
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a prompt exists.
        """

        file_path = self._prompt_directory / f"{name}.txt"

        return file_path.exists()

    def list(
        self,
    ) -> list[str]:
        """
        Return all available prompt names.
        """

        if not self._prompt_directory.exists():
            return []

        return sorted(
            file.stem
            for file in self._prompt_directory.glob("*.txt")
        )