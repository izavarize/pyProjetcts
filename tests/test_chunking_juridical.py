from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"


def test_chunks_have_legal_content():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT content
                FROM rag.document_chunks
                LIMIT 20
            """)
        ).scalars().all()

    assert rows, "Nenhum chunk encontrado"

    legal_markers = ["Art.", "art.", "§", "inciso", "caput"]

    matches = sum(
        any(marker in chunk for marker in legal_markers)
        for chunk in rows
    )

    assert matches >= 5, "Chunking jurídico parece inválido ou genérico"


def test_chunk_token_size_reasonable():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        token_counts = conn.execute(
            text("""
                SELECT token_count
                FROM rag.document_chunks
                LIMIT 50
            """)
        ).scalars().all()

    assert all(50 <= t <= 800 for t in token_counts), (
        "Chunks com tamanho fora do intervalo esperado (50–800 tokens)"
    )
