from fastapi import APIRouter, HTTPException

from app.api.schemas.provider_model_response import ModelResponse
from app.registry.model_registry import ModelRegistry

router = APIRouter(
    prefix="/providers",
    tags=["Providers"],
)


@router.get(
    "",
    response_model=list[str],
    summary="List supported AI providers",
)
def get_providers() -> list[str]:
    """
    Returns all supported AI providers.
    """
    return ModelRegistry.get_supported_providers()


@router.get(
    "/{provider}/models",
    response_model=list[ModelResponse],
    summary="List supported models for a provider",
)
def get_models(provider: str) -> list[ModelResponse]:
    """
    Returns all supported models for the requested provider.
    """

    models = ModelRegistry.get_models(provider)

    if not models:
        raise HTTPException(
            status_code=404,
            detail=f"Provider '{provider}' is not supported.",
        )

    return [
        ModelResponse(
            provider=model.provider,
            name=model.name,
            display_name=model.display_name,
            default=model.default,
            supports_streaming=model.supports_streaming,
        )
        for model in models
    ]