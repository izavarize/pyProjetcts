from collections.abc import Sequence
from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.domain.retrieval import RetrievedChunk


class PostgresVectorStore:
    """
    Armazenamento vetorial com busca híbrida: vetor (cosine) + full-text (tsvector).
    Combina scores com pesos configuráveis (alpha=vetor, beta=full-text).
    """

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
        # Busca híbrida: vetor + full-text (português).
        # JOIN em documents para obter source (compatível com schema sem source em chunks).
        # COALESCE no ts_rank_cd para quando search_vector for NULL (só vetor).
        # Normalização do FTS: ts_rank_cd pode ser > 1; usamos LEAST(ts_rank_cd, 1) para escala [0,1].
        sql = text(
            """
            WITH ranked AS (
                SELECT
                    d.source,
                    dc.content,
                    1 - (dc.embedding <=> :query_vec) AS vector_score,
                    LEAST(
                        COALESCE(
                            ts_rank_cd(
                                dc.search_vector,
                                plainto_tsquery('portuguese', :query),
                                32
                            ),
                            0
                        )::double precision,
                        1.0
                    ) AS fts_score
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
            )
            SELECT
                source,
                content,
                ( :alpha * vector_score + :beta * fts_score ) AS score
            FROM ranked
            WHERE ( :alpha * vector_score + :beta * fts_score ) >= :min_score
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
