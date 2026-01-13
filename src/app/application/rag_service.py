from app.infrastructure.rag.postgres_vector_store import PostgresVectorStore
from app.infrastructure.rag.local_embedder import LocalEmbedder
from app.domain.retrieval import RetrievedChunk
from app.core.database import engine


class RAGService:
    def __init__(self) -> None:
        self._embedder = LocalEmbedder()
        self._store = PostgresVectorStore(engine)
        self._min_score = 0.65

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        query_embedding = self._embedder.embed([query])[0]

        return self._store.search(
            query=query,
            query_embedding=query_embedding,
            limit=10,
            min_score=self._min_score,
        )
