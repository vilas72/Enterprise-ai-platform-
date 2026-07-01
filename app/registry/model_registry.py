from __future__ import annotations

from typing import Dict, List

from app.domain.models.model_info import ModelInfo


class ModelRegistry:
    """
    Enterprise AI Model Registry.

    Responsible for maintaining all supported AI models
    and their metadata.

    This registry acts as the single source of truth
    for model validation and default model resolution.
    """

    _models: Dict[str, List[ModelInfo]] = {
        "openai": [
            ModelInfo(
                provider="openai",
                name="gpt-4.1-mini",
                display_name="GPT-4.1 Mini",
                default=True,
                supports_streaming=True,
            ),
            ModelInfo(
                provider="openai",
                name="gpt-4.1",
                display_name="GPT-4.1",
                default=False,
                supports_streaming=True,
            ),
            ModelInfo(
                provider="openai",
                name="gpt-4o",
                display_name="GPT-4o",
                default=False,
                supports_streaming=True,
            ),
        ],
        "gemini": [
            ModelInfo(
                provider="gemini",
                name="gemini-2.5-pro",
                display_name="Gemini 2.5 Pro",
                default=True,
                supports_streaming=True,
            ),
            ModelInfo(
                provider="gemini",
                name="gemini-2.5-flash",
                display_name="Gemini 2.5 Flash",
                default=False,
                supports_streaming=True,
            ),
        ],
    }

    @classmethod
    def get_models(cls, provider: str) -> List[ModelInfo]:
        """
        Returns all supported models for a provider.
        """
        return cls._models.get(provider.lower(), [])

    @classmethod
    def get_default_model(cls, provider: str) -> ModelInfo | None:
        """
        Returns the default model for the specified provider.
        """
        for model in cls.get_models(provider):
            if model.default:
                return model
        return None

    @classmethod
    def get_model(
        cls,
        provider: str,
        model_name: str,
    ) -> ModelInfo | None:
        """
        Returns the requested model if it is supported.
        """
        for model in cls.get_models(provider):
            if model.name == model_name:
                return model
        return None

    @classmethod
    def is_supported(
        cls,
        provider: str,
        model_name: str,
    ) -> bool:
        """
        Checks whether the specified model is supported
        by the provider.
        """
        return cls.get_model(provider, model_name) is not None

    @classmethod
    def get_supported_providers(cls) -> List[str]:
        """
        Returns all registered providers.
        """
        return list(cls._models.keys())