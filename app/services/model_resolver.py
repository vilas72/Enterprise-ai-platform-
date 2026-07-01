from __future__ import annotations

from app.domain.models.model_info import ModelInfo
from app.domain.exceptions.validation_exception import ValidationException
from app.registry.model_registry import ModelRegistry


class ModelResolver:
    """
    Resolves AI models for a provider.

    Responsibilities:
        - Resolve default model
        - Validate requested model
        - Return ModelInfo
    """

    @staticmethod
    def resolve(
        provider: str,
        requested_model: str | None = None,
    ) -> ModelInfo:
        """
        Resolve the final model for a provider.

        Args:
            provider: Provider name.
            requested_model: Optional model supplied by the caller.

        Returns:
            ModelInfo

        Raises:
            ValidationException
        """

        provider = provider.lower()

        # Validate provider

        if provider not in ModelRegistry.get_supported_providers():
            raise ValidationException(
                message=f"Unsupported provider '{provider}'."
            )

        # Resolve default model

        if requested_model is None:

            model = ModelRegistry.get_default_model(provider)

            if model is None:
                raise ValidationException(
                    message=f"No default model configured for provider '{provider}'."
                )

            return model

        # Validate requested model

        model = ModelRegistry.get_model(
            provider=provider,
            model_name=requested_model,
        )

        if model is None:
            raise ValidationException(
            message=f"Model '{requested_model}' is not supported for provider '{provider}'.",
            field="model",
        )

        return model