from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TelemetryEvent:
    # Base
    timestamp: datetime
    operation: str
    duration_ms: float
    success: bool

    # LLM
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0

    # RAG
    retrieved_chunks: int = 0
    max_score: Optional[float] = None
    avg_score: Optional[float] = None
    min_score: Optional[float] = None
    coverage: Optional[float] = None
    used_fallback: bool = False

    # Erro
    error_type: Optional[str] = None
    error_message: Optional[str] = None
