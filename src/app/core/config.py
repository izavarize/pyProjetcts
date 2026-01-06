import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.google_api_key: str = self._get_required("GOOGLE_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    @staticmethod
    def _get_required(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Variável de ambiente obrigatória não configurada: {name}")
        return value


settings = Settings()
