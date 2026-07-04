from __future__ import annotations

import json

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # CORS
    # Accepts:
    # - "*" (allow all)
    # - JSON array string: ["https://a.com", "https://b.com"]
    # - Comma-separated string: https://a.com,https://b.com
    cors_origins: str = ""

    def cors_origins_list(self) -> list[str]:
        s = (self.cors_origins or "").strip()
        if not s:
            return []
        if s == "*":
            return ["*"]
        if s.startswith("[") and s.endswith("]"):
            try:
                data = json.loads(s)
                if isinstance(data, list):
                    return [str(x).strip() for x in data if str(x).strip()]
            except Exception:  # noqa: BLE001
                pass
        return [x.strip() for x in s.split(",") if x.strip()]


settings = Settings()  # type: ignore[call-arg]

