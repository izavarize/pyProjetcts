from typing import List
from app.infrastructure.rag.embedder import Embedder
from app.infrastructure.rag.vector_store import VectorStore
from app.domain.telemetry import TelemetryEvent
from datetime import datetime


class RAGService:
    def __init__(self, embedder: Embedder, store: VectorStore, min_score: float = 0.75):
        self._embedder = embedder
        self._store = store
        self._min_score = min_score

    def retrieve(self, query: str):
        query_embedding = self._embedder.embed([query])[0]

        results = self._store.search(
            query_embedding=query_embedding,
            limit=10,
            min_score=self._min_score,
        )

        if not results:
            return [], self._rag_metrics([])

        scores = [r.score for r in results]

        metrics = {
            "retrieved_chunks": len(results),
            "max_score": max(scores),
            "avg_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "coverage": len([s for s in scores if s >= self._min_score]) / len(scores),
            "used_fallback": False,
        }

        return results, metrics

    def _rag_metrics(self, results):
        return {
            "retrieved_chunks": 0,
            "max_score": None,
            "avg_score": None,
            "min_score": None,
            "coverage": 0.0,
            "used_fallback": True,
        }
