from app.domain.rag import DocumentChunk
from app.infrastructure.rag.embedder import GeminiEmbedder
from app.infrastructure.rag.vector_store import InMemoryVectorStore


class RAGService:
    def __init__(self) -> None:
        self._embedder = GeminiEmbedder()
        self._store = InMemoryVectorStore()

    def ingest(self, documents: list[DocumentChunk]) -> None:
        embeddings = self._embedder.embed([d.content for d in documents])
        self._store.add(embeddings, documents)

    def retrieve(self, query: str, top_k: int = 3) -> list[DocumentChunk]:
        query_embedding = self._embedder.embed([query])[0]
        results = self._store.search(query_embedding, top_k=top_k)

        return [DocumentChunk(r.content, r.source) for r in results]
