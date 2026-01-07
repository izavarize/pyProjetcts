import time

from google import genai

from app.core.logging import get_logger
from app.domain.telemetry import TelemetryEvent
from app.infrastructure.observability.telemetry_collector import TelemetryCollector

logger = get_logger("gemini")


class GeminiClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._telemetry = TelemetryCollector()

    def generate(self, prompt: str) -> str:
        start = self._telemetry.start_timer()

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        duration_ms = (time.perf_counter() - start) * 1000

        # Estimativa simples de tokens (SDK não retorna métricas precisas)
        input_tokens = len(prompt.split())
        output_text = response.text or ""
        output_tokens = len(output_text.split())

        # Estimativa conservadora de custo (ajustável depois)
        cost_usd = (input_tokens + output_tokens) * 0.00000025

        self._telemetry.record(
            TelemetryEvent(
                operation="generate_content",
                duration_ms=duration_ms,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
                mode="rag",  # o AIService define se é fallback
            )
        )

        logger.info(
            "llm_response",
            extra={
                "extra": {
                    "duration_ms": duration_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost_usd": cost_usd,
                }
            },
        )

        return output_text
