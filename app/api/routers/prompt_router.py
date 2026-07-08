from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.prompt.prompt_response import PromptResponse
from app.api.schemas.prompt.render_prompt_request import RenderPromptRequest
from app.dependencies.service_dependencies import get_prompt_service
from app.prompt.prompt_service import PromptService

router = APIRouter(
    prefix="/prompts",
    tags=["Prompt Management"],
)


@router.get(
    "",
    response_model=list[str],
)
def list_prompts(
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """
    List all available prompt templates.
    """

    return prompt_service.list_prompts()


@router.get(
    "/{name}",
    response_model=PromptResponse,
)
def get_prompt(
    name: str,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """
    Get a prompt template.
    """

    try:

        prompt = prompt_service.get_prompt(name)

        return PromptResponse(
            name=prompt.name,
            content=prompt.content,
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail=f"Prompt '{name}' not found.",
        )


@router.post(
    "/{name}/render",
    response_model=str,
)
def render_prompt(
    name: str,
    request: RenderPromptRequest,
    prompt_service: PromptService = Depends(get_prompt_service),
):
    """
    Render a prompt template.
    """

    try:

        return prompt_service.render_prompt(
            name=name,
            variables=request.variables,
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail=f"Prompt '{name}' not found.",
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )