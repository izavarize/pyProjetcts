from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # =========================
    # Ambiente / Log
    # =========================
    env: str = "local"
    log_level: str = "INFO"

    # =========================
    # IA / LLM
    # =========================
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    # =========================
    # Vector Store
    # =========================
    vector_store: str = "postgres"
    pg_dsn: str

    # =========================
    # RAG
    # =========================
    min_score: float = 0.75

    # 🔑 Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",  # <<< PERMITE VARIÁVEIS EXTRAS
    )


settings = Settings()
