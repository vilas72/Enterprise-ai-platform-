from app.prompt.prompt import Prompt
from app.prompt.prompt_renderer import PromptRenderer
from app.prompt.prompt_repository import PromptRepository


class PromptService:
    """
    Service responsible for loading and rendering prompts.
    """

    def __init__(
        self,
        repository: PromptRepository,
    ) -> None:
        self._repository = repository

    def get_prompt(
        self,
        name: str,
    ) -> Prompt:
        """
        Load a prompt by name.
        """

        return self._repository.get(name)

    def render_prompt(
        self,
        name: str,
        variables: dict[str, str] | None = None,
    ) -> str:
        """
        Load and render a prompt.
        """

        prompt = self._repository.get(name)

        missing = PromptRenderer.validate(
            prompt,
            variables,
        )

        if missing:
            raise ValueError(
                f"Missing prompt variables: {', '.join(missing)}"
            )

        return PromptRenderer.render(
            prompt,
            variables,
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if a prompt exists.
        """

        return self._repository.exists(name)

    def list_prompts(
        self,
    ) -> list[str]:
        """
        Return all available prompt names.
        """

        return self._repository.list()