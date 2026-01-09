from typing import List, Dict
from sqlalchemy import text
from app.infrastructure.persistence.db import engine


class PGVectorRetriever:
    """
    Recuperação vetorial SQL nativa com pgvector.
    """

    def search(
        self,
        query_vector: List[float],
        limit: int,
        min_score: float,
    ) -> List[Dict]:

        sql = text(
            """
            SELECT
                d.source,
                d.version,
                dc.content,
                dc.token_count,
                1 - (dc.embedding <=> :query_vec) AS score
            FROM document_chunks dc
            JOIN documents d ON d.id = dc.document_id
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

        return [
            {
                "source": r.source,
                "version": r.version,
                "content": r.content,
                "token_count": r.token_count,
                "score": float(r.score),
            }
            for r in rows
        ]
