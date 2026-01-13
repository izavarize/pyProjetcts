from collections.abc import Sequence
from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.domain.retrieval import RetrievedChunk


class PostgresVectorStore:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def search(
        self,
        query: str,
        query_embedding: Sequence[float],
        limit: int,
        min_score: float,
        alpha: float = 0.7,
        beta: float = 0.3,
    ) -> list[RetrievedChunk]:
        sql = text(
            """
            WITH ranked AS (
                SELECT
                    source,
                    content,
                    1 - (embedding <=> :query_vec) AS vector_score,
                    ts_rank_cd(
                        search_vector,
                        plainto_tsquery('portuguese', :query)
                    ) AS bm25_score
                FROM document_chunks
            )
            SELECT
                source,
                content,
                ( :alpha * vector_score + :beta * bm25_score ) AS score
            FROM ranked
            WHERE ( :alpha * vector_score + :beta * bm25_score ) >= :min_score
            ORDER BY score DESC
            LIMIT :limit
            """
        )

        with self._engine.connect() as conn:
            rows = conn.execute(
                sql,
                {
                    "query": query,
                    "query_vec": list(query_embedding),
                    "limit": limit,
                    "min_score": min_score,
                    "alpha": alpha,
                    "beta": beta,
                },
            ).fetchall()

        return [
            RetrievedChunk(
                source=row.source,
                content=row.content,
                score=float(row.score),
            )
            for row in rows
        ]
