import time

from app.core.logging import get_logger
from app.domain.telemetry import TelemetryEvent

logger = get_logger("telemetry")


class TelemetryCollector:
    def __init__(self) -> None:
        self._events: list[TelemetryEvent] = []

    def start_timer(self) -> float:
        return time.perf_counter()

    def record(self, event: TelemetryEvent) -> None:
        self._events.append(event)

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
