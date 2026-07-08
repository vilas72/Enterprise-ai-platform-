import re

from app.prompt.prompt import Prompt


class PromptRenderer:
    """
    Renders prompt templates by replacing variables.
    """

    VARIABLE_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    @classmethod
    def render(
        cls,
        prompt: Prompt,
        variables: dict[str, str] | None = None,
    ) -> str:

        if not variables:
            return prompt.content

        rendered = prompt.content

        for key, value in variables.items():

            rendered = rendered.replace(
                "{{" + key + "}}",
                str(value),
            )

        return rendered

    @classmethod
    def extract_variables(
        cls,
        prompt: Prompt,
    ) -> list[str]:

        return cls.VARIABLE_PATTERN.findall(
            prompt.content
        )

    @classmethod
    def validate(
        cls,
        prompt: Prompt,
        variables: dict[str, str] | None,
    ) -> list[str]:

        if variables is None:
            variables = {}

        required = set(
            cls.extract_variables(prompt)
        )

        provided = set(
            variables.keys()
        )

        return sorted(
            required - provided
        )