from fastapi import APIRouter
from sqlalchemy import text
from app.core.db import engine

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary")
def metrics_summary():
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT
                    count(*) as total_requests,
                    avg(duration_ms) as avg_latency,
                    sum(cost_usd) as total_cost,
                    sum(CASE WHEN success = false THEN 1 ELSE 0 END) as errors
                FROM telemetry_events
            """)
        ).mappings().first()

    return dict(result)
