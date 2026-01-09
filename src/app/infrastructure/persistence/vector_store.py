from typing import List, Tuple
from sqlalchemy import text
from app.infrastructure.persistence.db import engine


class VectorStore:
    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        min_score: float = 0.7,
    ) -> List[Tuple[str, str, float]]:

        sql = text(
            """
            SELECT
                dc.source,
                dc.content,
                1 - (dc.embedding <=> :query_vec) AS score
            FROM document_chunks dc
            WHERE 1 - (dc.embedding <=> :query_vec) >= :min_score
            ORDER BY dc.embedding <=> :query_vec
            LIMIT :limit
            """
        )

        with engine.connect() as conn:
            rows = conn.execute(
                sql,
                {
                    "query_vec": query_vector,
                    "limit": limit,
                    "min_score": min_score,
                },
            ).fetchall()

        return [(r.source, r.content, r.score) for r in rows]
