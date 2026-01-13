from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    """
    Representa um trecho recuperado pelo RAG.
    Objeto de domínio puro (sem dependência de infra).
    """

    source: str
    content: str
    score: float
