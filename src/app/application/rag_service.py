from app.domain.rag import DocumentChunk
from app.infrastructure.rag.token_chunker import TokenChunker
from app.infrastructure.rag.embedder import GeminiEmbedder
from app.infrastructure.rag.sqlite_vector_store import SQLiteVectorStore


class RAGService:
    def __init__(self) -> None:
        self._embedder = GeminiEmbedder()
        self._store = InMemoryVectorStore()
        self._chunker = TokenChunker(chunk_tokens=200, overlap_tokens=40)

    def ingest(self, documents: list[DocumentChunk]) -> None:
        chunks: list[DocumentChunk] = []

        for doc in documents:
            parts = self._chunker.chunk(doc.content)
            for i, part in enumerate(parts):
                chunks.append(
                    DocumentChunk(
                        content=part,
                        source=f"{doc.source}#chunk{i}",
                    )
                )

        embeddings = self._embedder.embed([c.content for c in chunks])
        self._store.add(embeddings, chunks)

    def retrieve(self, query: str, top_k: int = 3) -> list[DocumentChunk]:
        query_embedding = self._embedder.embed([query])[0]
        results = self._store.search(query_embedding, top_k=top_k)

        return [DocumentChunk(r.content, r.source) for r in results]
