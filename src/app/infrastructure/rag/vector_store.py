import numpy as np

from app.domain.rag import DocumentChunk, RetrievedChunk


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._vectors: list[np.ndarray] = []
        self._chunks: list[DocumentChunk] = []

    def add(self, vectors: list[list[float]], chunks: list[DocumentChunk]) -> None:
        for v, c in zip(vectors, chunks):
            self._vectors.append(np.array(v))
            self._chunks.append(c)

    def search(self, query_vector: list[float], top_k: int = 3) -> list[RetrievedChunk]:
        q = np.array(query_vector)

        scores = []
        for v in self._vectors:
            score = float(np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v)))
            scores.append(score)

        ranked = sorted(
            zip(self._chunks, scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        return [
            RetrievedChunk(
                content=chunk.content,
                source=chunk.source,
                score=score,
            )
            for chunk, score in ranked
        ]
