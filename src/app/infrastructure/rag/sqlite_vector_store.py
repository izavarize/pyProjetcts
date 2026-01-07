import json
import sqlite3
from pathlib import Path

import numpy as np

from app.domain.rag import DocumentChunk, RetrievedChunk


class SQLiteVectorStore:
    def __init__(self, db_path: str = "rag_vectors.db") -> None:
        self._path = Path(db_path)
        self._conn = sqlite3.connect(self._path)
        self._init_db()

    def _init_db(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def add(self, vectors: list[list[float]], chunks: list[DocumentChunk]) -> None:
        cur = self._conn.cursor()

        for vector, chunk in zip(vectors, chunks):
            cur.execute(
                """
                INSERT INTO vectors (source, content, embedding)
                VALUES (?, ?, ?)
                """,
                (
                    chunk.source,
                    chunk.content,
                    json.dumps(vector),
                ),
            )

        self._conn.commit()

    def search(self, query_vector: list[float], top_k: int = 3) -> list[RetrievedChunk]:
        cur = self._conn.cursor()
        cur.execute("SELECT source, content, embedding FROM vectors")

        rows = cur.fetchall()
        q = np.array(query_vector)

        scored = []

        for source, content, emb_json in rows:
            v = np.array(json.loads(emb_json))
            score = float(np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v)))

            scored.append(
                RetrievedChunk(
                    content=content,
                    source=source,
                    score=score,
                )
            )

        return sorted(scored, key=lambda x: x.score, reverse=True)[:top_k]
