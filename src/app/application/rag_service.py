from typing import List

from app.core.config import settings
from app.domain.rag import DocumentChunk
from app.infrastructure.rag.embedder import LocalEmbedder
from app.infrastructure.rag.postgres_vector_store import PostgresVectorStore


class RAGService:
    def __init__(self) -> None:
        self._embedder = LocalEmbedder()
        self._store = PostgresVectorStore(settings.pg_dsn)
        self._min_score = settings.min_score

    def ingest(self, docs: List[tuple[str, str]]) -> None:
        chunks = [
            DocumentChunk(content=content, source=source)
            for content, source in docs
        ]

        embeddings = self._embedder.embed([c.content for c in chunks])

        self._store.upsert(chunks, embeddings)

    def retrieve(self, query: str) -> List[DocumentChunk]:
        query_embedding = self._embedder.embed([query])[0]

        return self._store.search(
            query_embedding=query_embedding,
            limit=10,
            min_score=self._min_score,
        )
