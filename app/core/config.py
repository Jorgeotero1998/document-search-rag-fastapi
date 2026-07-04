from __future__ import annotations

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "backend-portfolio-template"
    env: str = "local"
    log_level: str = "INFO"

    # security
    jwt_secret: str
    jwt_access_ttl_seconds: int = 900
    jwt_refresh_ttl_seconds: int = 60 * 60 * 24 * 14

    # db
    database_url: str

    # redis/celery (optional in production; required only for projects that use it)
    redis_url: str | None = None
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None

    # ai (optional)
    llm_enabled: bool = False
    llm_provider: str = "groq"
    llm_api_key: str = ""
    llm_base_url: AnyUrl | None = None
    llm_model: str = "llama-3.1-8b-instant"

    # CORS (comma-separated origins)
    cors_origins: list[str] = []

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        s = str(v).strip()
        if not s:
            return []
        return [x.strip() for x in s.split(",") if x.strip()]


settings = Settings()  # type: ignore[call-arg]

