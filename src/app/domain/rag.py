from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    content: str
    source: str


@dataclass(frozen=True)
class RetrievedChunk:
    content: str
    source: str
    score: float
