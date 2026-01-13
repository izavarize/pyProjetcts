from fastapi import FastAPI

from app.api.routers.ask import router as ask_router
from app.api.routers.health import router as health_router
from app.api.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(
    title="TaxSearch API",
    version="0.1.0",
    description="RAG jurídico com Gemini",
)

app.add_middleware(
    RateLimitMiddleware,
    max_requests=20,
    window_seconds=60,
)

app.include_router(ask_router)
app.include_router(health_router)
