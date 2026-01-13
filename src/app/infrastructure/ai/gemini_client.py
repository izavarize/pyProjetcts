from typing import Optional

from google.genai import Client
from google.genai.errors import APIError


class GeminiClient:
    """
    Client de integração com o Google Gemini.

    Responsabilidade:
    - Enviar prompts para o Gemini
    - Retornar apenas texto processado
    - NÃO conter regras de negócio
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash"
    ) -> None:
        if not api_key:
            raise ValueError("Gemini API key não informada.")

        self.model = model
        self.client = Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Envia um prompt para o Gemini e retorna o texto gerado.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt vazio ou inválido.")

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            if not response or not response.text:
                raise RuntimeError("Resposta vazia retornada pelo Gemini.")

            return response.text.strip()

        except APIError as exc:
            raise RuntimeError(
                f"Erro ao comunicar com a API do Gemini: {exc}"
            ) from exc

        except Exception as exc:
            raise RuntimeError(
                f"Erro inesperado ao gerar resposta com Gemini: {exc}"
            ) from exc
