from typing import List, Dict
from app.infrastructure.rag.pgvector_retriever import PGVectorRetriever


class RAGRetriever:
    """
    Orquestra a recuperação vetorial com filtros de score.
    """

    def __init__(self, min_score: float = 0.75, limit: int = 8):
        self._min_score = min_score
        self._limit = limit
        self._store = PGVectorRetriever()

    def retrieve(self, query_vector: List[float]) -> List[Dict]:
        return self._store.search(
            query_vector=query_vector,
            limit=self._limit,
            min_score=self._min_score,
        )
