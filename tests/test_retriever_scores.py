from sqlalchemy import create_engine, text
from app.infrastructure.ai.gemini_client import GeminiClient
from app.application.embedding.embedding_service import EmbeddingService

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"


def test_retrieval_score_threshold():
    query = "O que dispõe o artigo 3º da Constituição Federal?"

    engine = create_engine(DATABASE_URL)
    ai = GeminiClient()
    embedder = EmbeddingService(ai)

    query_vector = embedder.embed(query)

    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT
                    1 - (embedding <=> :query_vec) AS score
                FROM rag.document_chunks
                ORDER BY embedding <=> :query_vec
                LIMIT 5
            """),
            {"query_vec": query_vector}
        ).scalars().all()

    assert rows, "Nenhum resultado retornado pelo retriever"
    assert rows[0] >= 0.75, f"Score semântico baixo demais: {rows[0]}"


def test_retrieval_returns_cf_content():
    query = "fundamentos da República Federativa do Brasil"

    engine = create_engine(DATABASE_URL)
    ai = GeminiClient()
    embedder = EmbeddingService(ai)

    query_vector = embedder.embed(query)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT d.source, dc.content
                FROM rag.document_chunks dc
                JOIN rag.documents d ON d.id = dc.document_id
                ORDER BY dc.embedding <=> :query_vec
                LIMIT 1
            """),
            {"query_vec": query_vector}
        ).first()

    assert result is not None, "Nenhum conteúdo recuperado"
    assert "Constituição" in result.source, "Documento incorreto recuperado"
