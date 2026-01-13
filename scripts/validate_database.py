from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"


CHECKS = [
    "SELECT * FROM rag.rag_health_check();",
    "SELECT COUNT(*) FROM rag.documents;",
    "SELECT COUNT(*) FROM rag.document_chunks;",
]


def main():
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        print("\n=== Health Check RAG ===")
        result = conn.execute(text(CHECKS[0]))
        for row in result:
            print(f"{row.check_name}: {row.status}")

        print("\n=== Contagem de Dados ===")
        docs = conn.execute(text(CHECKS[1])).scalar()
        chunks = conn.execute(text(CHECKS[2])).scalar()

        print(f"Documents: {docs}")
        print(f"Document Chunks: {chunks}")

        if docs == 0:
            print("⚠ Nenhum documento cadastrado.")
        if chunks == 0:
            print("⚠ Nenhum chunk indexado.")


if __name__ == "__main__":
    main()
