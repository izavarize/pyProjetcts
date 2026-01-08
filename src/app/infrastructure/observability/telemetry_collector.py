import time
from sqlalchemy import create_engine

from app.core.config import settings
from app.core.logging import get_logger
from app.domain.telemetry import TelemetryEvent
from app.infrastructure.observability.telemetry_repository import TelemetryRepository

logger = get_logger("telemetry")


class TelemetryCollector:
    def __init__(self) -> None:
        engine = create_engine(settings.pg_dsn)
        self._repository = TelemetryRepository(engine)

    def start_timer(self) -> float:
        return time.perf_counter()

    def record(self, event: TelemetryEvent) -> None:
        # Persistência
        self._repository.save(event)

        # Log estruturado
        logger.info(
            "telemetry_event",
            extra={
                "extra": {
                    "operation": event.operation,
                    "duration_ms": event.duration_ms,
                    "input_tokens": event.input_tokens,
                    "output_tokens": event.output_tokens,
                    "cost_usd": event.cost_usd,
                    "mode": event.mode,
                }
            },
        )
