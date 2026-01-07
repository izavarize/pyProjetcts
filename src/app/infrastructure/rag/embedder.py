from google import genai

from app.core.config import settings


class GeminiEmbedder:
    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.google_api_key)

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._client.models.embed_content(
            model="text-embedding-004",
            contents=texts,
        )

        return [e.values for e in response.embeddings]
