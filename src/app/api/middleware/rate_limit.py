from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.infrastructure.rate_limit.simple_rate_limiter import SimpleRateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        max_requests: int = 20,
        window_seconds: int = 60,
    ) -> None:
        super().__init__(app)
        self._limiter = SimpleRateLimiter(
            max_requests=max_requests,
            window_seconds=window_seconds,
        )

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        if not self._limiter.allow(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
            )

        return await call_next(request)
