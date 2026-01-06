from google import genai

from app.infrastructure.ai.llm_client import LLMClient


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str):
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config={
                "temperature": 0.2,
            },
        )

        if not response.text:
            raise RuntimeError("Resposta vazia do Gemini")

        return response.text.strip()
