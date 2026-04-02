from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Human-readable application name
    app_name: str = Field(default="Voyagr API", validation_alias="APP_NAME")

    # Current runtime environment
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        validation_alias="APP_ENV",
    )

    # Enables development-friendly behavior when True
    debug: bool = Field(default=True, validation_alias="DEBUG")

    # Controls logging verbosity
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Shared API prefix for versioned routes
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="API_V1_PREFIX")

    # Primary LLM provider key for early Voyagr examples
    groq_api_key: str | None = Field(default=None, validation_alias="GROQ_API_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()
