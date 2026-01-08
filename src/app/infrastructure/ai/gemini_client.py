import time

from google import genai
from google.genai.errors import ClientError

from app.core.logging import get_logger
from app.domain.telemetry import TelemetryEvent
from app.infrastructure.ai.llm_client import LLMClient
from app.infrastructure.observability.telemetry_collector import TelemetryCollector

logger = get_logger("gemini")


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._telemetry = TelemetryCollector()

    def generate(self, prompt: str) -> str:
        start = time.perf_counter()

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
            )

            output_text = response.text or ""

            duration_ms = (time.perf_counter() - start) * 1000
            input_tokens = len(prompt.split())
            output_tokens = len(output_text.split())
            cost_usd = (input_tokens + output_tokens) * 0.00000025

            self._telemetry.record(
                TelemetryEvent(
                    operation="generate_content",
                    duration_ms=duration_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=cost_usd,
                    mode="rag",
                )
            )

            return output_text

        except ClientError as exc:
            if exc.code == 429:
                logger.warning(
                    "gemini_quota_exceeded",
                    extra={"extra": {"code": exc.code, "message": str(exc)}},
                )

                self._telemetry.record(
                    TelemetryEvent(
                        operation="generate_content_quota_exceeded",
                        duration_ms=0.0,
                        input_tokens=0,
                        output_tokens=0,
                        cost_usd=0.0,
                        mode="error",
                    )
                )

                return (
                    "No momento, não é possível processar a solicitação devido "
                    "a limites temporários de uso do serviço de IA. "
                    "Por favor, tente novamente mais tarde."
                )

            raise
