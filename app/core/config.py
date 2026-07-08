import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

from app.core.constants import (
    DEFAULT_AZURE_OPENAI_MODEL,
    DEFAULT_BEDROCK_MODEL,
    DEFAULT_GEMINI_MODEL,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_PROVIDER,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ENV_FILE,
    ProviderName,
)

from app.core.constants import (
    DEFAULT_OPENAI_EMBEDDING_MODEL,
    DEFAULT_GEMINI_EMBEDDING_MODEL,
)

load_dotenv(ENV_FILE)


class ProviderSettings(BaseModel):
    name: ProviderName
    api_key: str | None = None
    model: str
    embedding_model: str | None = None
    base_url: str | None = None
    enabled: bool = True
    timeout_seconds: int = Field(default=DEFAULT_REQUEST_TIMEOUT_SECONDS, ge=1)
    max_retries: int = Field(default=DEFAULT_MAX_RETRIES, ge=0)


class BedrockSettings(BaseModel):
    name: ProviderName = ProviderName.BEDROCK
    model: str = DEFAULT_BEDROCK_MODEL
    region: str | None = None
    enabled: bool = False
    timeout_seconds: int = Field(default=DEFAULT_REQUEST_TIMEOUT_SECONDS, ge=1)
    max_retries: int = Field(default=DEFAULT_MAX_RETRIES, ge=0)


class AzureOpenAISettings(BaseModel):
    name: ProviderName = ProviderName.AZURE_OPENAI
    api_key: str | None = None
    model: str = DEFAULT_AZURE_OPENAI_MODEL
    endpoint: str | None = None
    deployment: str | None = None
    api_version: str | None = None
    enabled: bool = False
    timeout_seconds: int = Field(default=DEFAULT_REQUEST_TIMEOUT_SECONDS, ge=1)
    max_retries: int = Field(default=DEFAULT_MAX_RETRIES, ge=0)


class Settings(BaseModel):
    app_name: str = "Enterprise AI Platform"
    environment: str = "development"
    log_level: str = DEFAULT_LOG_LEVEL
    default_provider: ProviderName = DEFAULT_PROVIDER
    openai: ProviderSettings
    gemini: ProviderSettings
    bedrock: BedrockSettings
    azure_openai: AzureOpenAISettings

    @field_validator("environment")
    @classmethod
    def normalize_environment(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.strip().upper()

    def provider(
        self, name: ProviderName | str | None = None
    ) -> ProviderSettings | BedrockSettings | AzureOpenAISettings:
        provider_name = ProviderName(name or self.default_provider)
        return getattr(self, provider_name.value)


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def _env_bool(name: str, default: bool) -> bool:
    value = _env(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = _env(name)
    if value is None:
        return default
    return int(value)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=_env("APP_NAME", "Enterprise AI Platform") or "Enterprise AI Platform",
        environment=_env("ENVIRONMENT", "development") or "development",
        log_level=_env("LOG_LEVEL", DEFAULT_LOG_LEVEL) or DEFAULT_LOG_LEVEL,
        default_provider=ProviderName(_env("DEFAULT_PROVIDER", DEFAULT_PROVIDER.value)),
        openai=ProviderSettings(
                name=ProviderName.OPENAI,
                api_key=_env("OPENAI_API_KEY"),
                model=_env("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
                    or DEFAULT_OPENAI_MODEL,
                embedding_model=_env(
                    "OPENAI_EMBEDDING_MODEL",
                    DEFAULT_OPENAI_EMBEDDING_MODEL,
                )
                or DEFAULT_OPENAI_EMBEDDING_MODEL,
                base_url=_env("OPENAI_BASE_URL"),
                enabled=_env_bool("OPENAI_ENABLED", True),
                timeout_seconds=_env_int(
                    "OPENAI_TIMEOUT_SECONDS",
                    DEFAULT_REQUEST_TIMEOUT_SECONDS,
                ),
                max_retries=_env_int(
                    "OPENAI_MAX_RETRIES",
                    DEFAULT_MAX_RETRIES,
                ),
            ),
        gemini=ProviderSettings(
                name=ProviderName.GEMINI,
                api_key=_env("GEMINI_API_KEY"),
                model=_env(
                    "GEMINI_MODEL",
                    DEFAULT_GEMINI_MODEL,
                )
                or DEFAULT_GEMINI_MODEL,
                embedding_model=_env(
                    "GEMINI_EMBEDDING_MODEL",
                    DEFAULT_GEMINI_EMBEDDING_MODEL,
                )
                or DEFAULT_GEMINI_EMBEDDING_MODEL,
                base_url=_env("GEMINI_BASE_URL"),
                enabled=_env_bool("GEMINI_ENABLED", True),
                timeout_seconds=_env_int(
                    "GEMINI_TIMEOUT_SECONDS",
                    DEFAULT_REQUEST_TIMEOUT_SECONDS,
                ),
                max_retries=_env_int(
                    "GEMINI_MAX_RETRIES",
                    DEFAULT_MAX_RETRIES,
                ),
            ),
        bedrock=BedrockSettings(
            model=_env("BEDROCK_MODEL", DEFAULT_BEDROCK_MODEL)
            or DEFAULT_BEDROCK_MODEL,
            region=_env("AWS_REGION"),
            enabled=_env_bool("BEDROCK_ENABLED", False),
            timeout_seconds=_env_int(
                "BEDROCK_TIMEOUT_SECONDS", DEFAULT_REQUEST_TIMEOUT_SECONDS
            ),
            max_retries=_env_int("BEDROCK_MAX_RETRIES", DEFAULT_MAX_RETRIES),
        ),
        azure_openai=AzureOpenAISettings(
            api_key=_env("AZURE_OPENAI_API_KEY"),
            model=_env("AZURE_OPENAI_MODEL", DEFAULT_AZURE_OPENAI_MODEL)
            or DEFAULT_AZURE_OPENAI_MODEL,
            endpoint=_env("AZURE_OPENAI_ENDPOINT"),
            deployment=_env("AZURE_OPENAI_DEPLOYMENT"),
            api_version=_env("AZURE_OPENAI_API_VERSION"),
            enabled=_env_bool("AZURE_OPENAI_ENABLED", False),
            timeout_seconds=_env_int(
                "AZURE_OPENAI_TIMEOUT_SECONDS", DEFAULT_REQUEST_TIMEOUT_SECONDS
            ),
            max_retries=_env_int("AZURE_OPENAI_MAX_RETRIES", DEFAULT_MAX_RETRIES),
        ),
    )


settings = get_settings()
