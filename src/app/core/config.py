from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    env: str = Field(default="local")
    log_level: str = Field(default="INFO")

    # LLM
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash")

    # RAG
    min_score: float = Field(default=0.75)
    # Híbrido: peso vetor (alpha) + peso full-text (beta); alpha + beta = 1
    rag_hybrid_alpha: float = Field(default=0.7, description="Peso da busca vetorial")
    rag_hybrid_beta: float = Field(default=0.3, description="Peso da busca full-text")

    # Database
    pg_dsn: str = Field(..., env="PG_DSN")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
