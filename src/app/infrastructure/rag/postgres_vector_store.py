import uuid
from typing import List

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.domain.rag import DocumentChunk


class PostgresVectorStore:
    def __init__(self, dsn: str) -> None:
        self._engine: Engine = create_engine(dsn)

    def upsert(
        self,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
    ) -> None:
        sql = text(
            """
            INSERT INTO vectors (id, source, content, embedding)
            VALUES (:id, :source, :content, :embedding)
            """
        )

        with self._engine.begin() as conn:
            for chunk, embedding in zip(chunks, embeddings):
                conn.execute(
                    sql,
                    {
                        "id": str(uuid.uuid4()),
                        "source": chunk.source,
                        "content": chunk.content,
                        "embedding": embedding,
                    },
                )

    def search(
        self,
        query_embedding: List[float],
        limit: int,
        min_score: float,
    ) -> List[DocumentChunk]:
        """
        Busca vetorial por similaridade de cosseno (pgvector).
        """

        sql = text(
            """
            SELECT
                source,
                content,
                1 - (embedding <=> (:query_vec)::vector) AS score
            FROM vectors
            WHERE 1 - (embedding <=> (:query_vec)::vector) >= :min_score
            ORDER BY embedding <=> (:query_vec)::vector
            LIMIT :limit
            """
        )

        with self._engine.begin() as conn:
            rows = conn.execute(
                sql,
                {
                    "query_vec": query_embedding,
                    "limit": limit,
                    "min_score": min_score,
                },
            ).fetchall()

        return [
            DocumentChunk(
                content=row.content,
                source=row.source,
            )
            for row in rows
        ]
