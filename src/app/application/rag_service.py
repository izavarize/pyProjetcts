from app.core.config import settings
from app.domain.rag import DocumentChunk
from app.infrastructure.rag.token_chunker import TokenChunker
from app.infrastructure.rag.embedder import GeminiEmbedder
from app.infrastructure.rag.sqlite_vector_store import SQLiteVectorStore
from app.infrastructure.rag.postgres_vector_store import PostgresVectorStore


class RAGService:
    def __init__(self) -> None:
        self._embedder = GeminiEmbedder()
        self._chunker = TokenChunker(chunk_tokens=200, overlap_tokens=40)
        self._min_score = settings.min_score

        if settings.vector_store == "postgres":
            self._store = PostgresVectorStore(settings.pg_dsn)
        else:
            self._store = SQLiteVectorStore("rag.db")

    def ingest(self, documents: list[DocumentChunk]) -> None:
        chunks: list[DocumentChunk] = []

        for doc in documents:
            parts = self._chunker.chunk(doc.content)
            for idx, part in enumerate(parts):
                chunks.append(
                    DocumentChunk(
                        content=part,
                        source=f"{doc.source}#chunk{idx}",
                    )
                )

        if not chunks:
            return

        embeddings = self._embedder.embed([c.content for c in chunks])
        self._store.add(embeddings, chunks)

    def retrieve(self, query: str, top_k: int = 5) -> list[DocumentChunk]:
        query_embedding = self._embedder.embed([query])[0]

        results = self._store.search(
            query=query,
            query_vector=query_embedding,
            top_k=top_k,
            min_score=self._min_score,
        )

        return [
            DocumentChunk(
                content=r.content,
                source=r.source,
            )
            for r in results
        ]
