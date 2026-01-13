import pathlib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.infrastructure.ai.gemini_client import GeminiClient
from app.application.embedding.embedding_service import EmbeddingService
from app.application.ingestion.chunker import TextChunker

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"

DATA_DIR = pathlib.Path(__file__).parent / "data"


def ingest_document(file_path: pathlib.Path):
    engine = create_engine(DATABASE_URL)
    ai_client = GeminiClient()
    embedder = EmbeddingService(ai_client)
    chunker = TextChunker()

    content = file_path.read_text(encoding="utf-8")

    with Session(engine) as session:
        doc = session.execute(
            text("""
                SELECT id
                FROM rag.documents
                WHERE source = :source
            """),
            {"source": "Constituição Federal"}
        ).fetchone()

        if not doc:
            raise RuntimeError("Documento CF/88 não encontrado. Execute o seed primeiro.")

        document_id = doc.id

        chunks = chunker.split(content)

        for idx, chunk in enumerate(chunks):
            embedding = embedder.embed(chunk)

            session.execute(
                text("""
                    INSERT INTO rag.document_chunks (
                        document_id,
                        chunk_index,
                        content,
                        token_count,
                        embedding
                    )
                    VALUES (
                        :document_id,
                        :chunk_index,
                        :content,
                        :token_count,
                        :embedding
                    )
                """),
                {
                    "document_id": document_id,
                    "chunk_index": idx,
                    "content": chunk,
                    "token_count": len(chunk.split()),
                    "embedding": embedding
                }
            )

        session.commit()

    print(f"Ingestão concluída: {file_path.name}")


def main():
    for file in DATA_DIR.glob("*.txt"):
        ingest_document(file)


if __name__ == "__main__":
    main()
