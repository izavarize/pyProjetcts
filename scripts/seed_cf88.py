import pathlib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import date

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"

CF_SOURCE = "Constituição Federal"
CF_VERSION = "CF/88"
CF_TYPE = "CF"

BASE_DIR = pathlib.Path(__file__).parent
CF_FILE = BASE_DIR / "data" / "cf88.txt"


def main():
    if not CF_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CF_FILE}")

    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        # Evita duplicidade
        exists = conn.execute(
            text("""
                SELECT 1
                FROM rag.documents
                WHERE source = :source
                  AND version = :version
            """),
            {"source": CF_SOURCE, "version": CF_VERSION}
        ).scalar()

        if exists:
            print("CF/88 já cadastrada. Seed ignorado.")
            return

        conn.execute(
            text("""
                INSERT INTO rag.documents (
                    source,
                    version,
                    document_type,
                    description,
                    published_at
                )
                VALUES (
                    :source,
                    :version,
                    :type,
                    :description,
                    :published_at
                )
            """),
            {
                "source": CF_SOURCE,
                "version": CF_VERSION,
                "type": CF_TYPE,
                "description": "Constituição da República Federativa do Brasil de 1988",
                "published_at": date(1988, 10, 5)
            }
        )

    print("Seed da CF/88 criado com sucesso.")


if __name__ == "__main__":
    main()
