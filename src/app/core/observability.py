import time
from datetime import datetime
from functools import wraps
from app.domain.telemetry import TelemetryEvent


def observe(operation: str, telemetry_repo):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start) * 1000

                event = TelemetryEvent(
                    timestamp=datetime.utcnow(),
                    operation=operation,
                    duration_ms=duration,
                    success=True,
                )
                telemetry_repo.save(event)
                return result

            except Exception as exc:
                duration = (time.perf_counter() - start) * 1000
                event = TelemetryEvent(
                    timestamp=datetime.utcnow(),
                    operation=operation,
                    duration_ms=duration,
                    success=False,
                    error_type=type(exc).__name__,
                    error_message=str(exc),
                )
                telemetry_repo.save(event)
                raise

        return wrapper
    return decorator
