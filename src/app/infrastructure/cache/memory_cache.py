import time
import threading
from typing import Any


class MemoryCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl = ttl_seconds
        self._data: dict[str, tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            item = self._data.get(key)
            if not item:
                return None

            expires_at, value = item
            if time.time() > expires_at:
                del self._data[key]
                return None

            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = (time.time() + self._ttl, value)
