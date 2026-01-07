from sqlalchemy import text
from sqlalchemy.engine import Engine


class DocumentRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def exists_by_hash(self, content_hash: str) -> bool:
        query = text(
            """
            SELECT 1
            FROM documents
            WHERE content_hash = :hash
            LIMIT 1
            """
        )

        with self._engine.connect() as conn:
            result = conn.execute(query, {"hash": content_hash}).fetchone()
            return result is not None

    def save(self, source: str, content_hash: str) -> None:
        query = text(
            """
            INSERT INTO documents (source, content_hash)
            VALUES (:source, :hash)
            """
        )

        with self._engine.begin() as conn:
            conn.execute(
                query,
                {"source": source, "hash": content_hash},
            )
