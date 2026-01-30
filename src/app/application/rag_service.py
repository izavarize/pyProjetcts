from app.infrastructure.rag.postgres_vector_store import PostgresVectorStore
from app.infrastructure.rag.local_embedder import LocalEmbedder
from app.domain.retrieval import RetrievedChunk
from app.core.database import engine
from app.core.config import settings


class RAGService:
    """
    Serviço RAG híbrido: busca vetorial (pgvector) + full-text (tsvector).
    """

    def __init__(
        self,
        min_score: float | None = None,
        limit: int = 10,
        alpha: float | None = None,
        beta: float | None = None,
    ) -> None:
        self._embedder = LocalEmbedder()
        self._store = PostgresVectorStore(engine)
        self._min_score = min_score if min_score is not None else settings.min_score
        self._limit = limit
        self._alpha = alpha if alpha is not None else settings.rag_hybrid_alpha
        self._beta = beta if beta is not None else settings.rag_hybrid_beta

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        query_embedding = self._embedder.embed([query])[0]

        return self._store.search(
            query=query,
            query_embedding=query_embedding,
            limit=self._limit,
            min_score=self._min_score,
            alpha=self._alpha,
            beta=self._beta,
        )
