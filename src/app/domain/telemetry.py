from dataclasses import dataclass
from typing import Literal


@dataclass
class TelemetryEvent:
    operation: str
    duration_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    mode: Literal["rag", "fallback"]
