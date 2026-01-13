import time
import threading


class SimpleRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self._max = max_requests
        self._window = window_seconds
        self._hits: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str) -> bool:
        now = time.time()

        with self._lock:
            timestamps = self._hits.get(key, [])
            timestamps = [t for t in timestamps if now - t < self._window]

            if len(timestamps) >= self._max:
                self._hits[key] = timestamps
                return False

            timestamps.append(now)
            self._hits[key] = timestamps
            return True
