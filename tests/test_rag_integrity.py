from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"


def test_rag_schema_exists():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        exists = conn.execute(
            text("""
                SELECT 1
                FROM information_schema.schemata
                WHERE schema_name = 'rag'
            """)
        ).scalar()

    assert exists == 1, "Schema 'rag' não existe"


def test_core_tables_exist():
    engine = create_engine(DATABASE_URL)

    tables = {"documents", "document_chunks"}

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'rag'
            """)
        ).scalars().all()

    assert tables.issubset(set(result)), "Tabelas essenciais do RAG ausentes"


def test_embeddings_dimension():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        dim = conn.execute(
            text("""
                SELECT vector_dims(embedding)
                FROM rag.document_chunks
                LIMIT 1
            """)
        ).scalar()

    assert dim == 3072, f"Dimensão de embedding inválida: {dim}"
