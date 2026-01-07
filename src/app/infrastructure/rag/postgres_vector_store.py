from typing import Iterable

from sqlalchemy import text, create_engine
from sqlalchemy.engine import Engine

from app.domain.rag import DocumentChunk, RetrievedChunk
from app.infrastructure.rag.keyword_scorer import KeywordScorer


class PostgresVectorStore:
    def __init__(self, dsn: str) -> None:
        self._engine: Engine = create_engine(dsn)
        self._keyword = KeywordScorer()

    def add(self, vectors: list[list[float]], chunks: list[DocumentChunk]) -> None:
        insert_sql = text(
            """
            INSERT INTO vectors (source, content, embedding)
            VALUES (:source, :content, :embedding)
            """
        )

        with self._engine.begin() as conn:
            for vector, chunk in zip(vectors, chunks):
                conn.execute(
                    insert_sql,
                    {
                        "source": chunk.source,
                        "content": chunk.content,
                        "embedding": vector,
                    },
                )

    def search(
        self,
        query: str,
        query_vector: list[float],
        top_k: int = 10,
        min_score: float = 0.75,
    ) -> list[RetrievedChunk]:
        """
        Busca vetorial feita no SQL usando <=> (cosine distance).
        Re-rank híbrido (vetor + keyword) no Python.
        """

        sql = text(
            """
            SELECT
                source,
                content,
                1 - (embedding <=> :query_vec) AS vector_score
            FROM vectors
            ORDER BY embedding <=> :query_vec
            LIMIT :limit
            """
        )

        with self._engine.connect() as conn:
            rows = conn.execute(
                sql,
                {
                    "query_vec": query_vector,
                    "limit": top_k * 2,  # margem para re-rank
                },
            ).fetchall()

        results: list[RetrievedChunk] = []

        for row in rows:
            vector_score = float(row.vector_score)
            keyword_score = self._keyword.score(query, row.content)

            final_score = (0.7 * vector_score) + (0.3 * keyword_score)

            if final_score >= min_score:
                results.append(
                    RetrievedChunk(
                        content=row.content,
                        source=row.source,
                        score=final_score,
                    )
                )

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
