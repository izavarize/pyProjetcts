from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    MetaData,
)
from sqlalchemy.engine import Engine
from datetime import datetime

metadata = MetaData()

telemetry_table = Table(
    "telemetry_events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime, default=datetime.utcnow),

    Column("operation", String, nullable=False),
    Column("duration_ms", Float, nullable=False),
    Column("success", Boolean, nullable=False),

    # LLM
    Column("input_tokens", Integer),
    Column("output_tokens", Integer),
    Column("cost_usd", Float),

    # RAG
    Column("retrieved_chunks", Integer),
    Column("max_score", Float),
    Column("avg_score", Float),
    Column("min_score", Float),
    Column("coverage", Float),
    Column("used_fallback", Boolean),

    # Erros
    Column("error_type", String),
    Column("error_message", String),
)


class PostgresTelemetryRepository:
    def __init__(self, engine: Engine):
        metadata.create_all(engine)
        self._engine = engine

    def save(self, event):
        with self._engine.begin() as conn:
            conn.execute(
                telemetry_table.insert().values(
                    timestamp=event.timestamp,
                    operation=event.operation,
                    duration_ms=event.duration_ms,
                    success=event.success,

                    input_tokens=event.input_tokens,
                    output_tokens=event.output_tokens,
                    cost_usd=event.cost_usd,

                    retrieved_chunks=event.retrieved_chunks,
                    max_score=event.max_score,
                    avg_score=event.avg_score,
                    min_score=event.min_score,
                    coverage=event.coverage,
                    used_fallback=event.used_fallback,

                    error_type=event.error_type,
                    error_message=event.error_message,
                )
            )
