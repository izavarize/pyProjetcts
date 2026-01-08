from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.domain.telemetry import TelemetryEvent


class TelemetryRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def save(self, event: TelemetryEvent) -> None:
        query = text(
            """
            INSERT INTO telemetry_events (
                operation,
                duration_ms,
                input_tokens,
                output_tokens,
                cost_usd,
                mode
            )
            VALUES (
                :operation,
                :duration_ms,
                :input_tokens,
                :output_tokens,
                :cost_usd,
                :mode
            )
            """
        )

        with self._engine.begin() as conn:
            conn.execute(
                query,
                {
                    "operation": event.operation,
                    "duration_ms": event.duration_ms,
                    "input_tokens": event.input_tokens,
                    "output_tokens": event.output_tokens,
                    "cost_usd": event.cost_usd,
                    "mode": event.mode,
                },
            )
