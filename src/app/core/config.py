import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega explicitamente o .env da raiz do projeto
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


class Settings:
    def __init__(self) -> None:
        self.google_api_key = self._required("GOOGLE_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @staticmethod
    def _required(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Variável obrigatória não definida: {name}")
        return value


settings = Settings()
