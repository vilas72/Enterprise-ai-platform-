from enum import StrEnum


class ProviderName(StrEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
    BEDROCK = "bedrock"
    AZURE_OPENAI = "azure_openai"


DEFAULT_PROVIDER = ProviderName.OPENAI

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
DEFAULT_BEDROCK_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
DEFAULT_AZURE_OPENAI_MODEL = "gpt-4o-mini"

DEFAULT_REQUEST_TIMEOUT_SECONDS = 30
DEFAULT_MAX_RETRIES = 3
DEFAULT_LOG_LEVEL = "INFO"
ENV_FILE = ".env"
