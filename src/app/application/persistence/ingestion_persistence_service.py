from typing import List
from sqlalchemy import select, func

from app.domain.document import Document
from app.domain.document_chunk import DocumentChunk

from app.infrastructure.persistence.db import SessionLocal
from app.infrastructure.persistence.models import (
    DocumentModel,
    DocumentChunkModel,
)


class IngestionPersistenceService:
    """
    Aplica versionamento jurídico e persiste documentos e chunks.
    """

    def persist(
        self,
        document: Document,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
    ) -> None:

        session = SessionLocal()
        try:
            # 1️⃣ Deduplicação por hash
            existing = session.execute(
                select(DocumentModel).where(
                    DocumentModel.content_hash == document.content_hash
                )
            ).scalar_one_or_none()

            if existing:
                return  # documento idêntico já existe

            # 2️⃣ Determinar próxima versão
            max_version = session.execute(
                select(func.max(DocumentModel.version)).where(
                    DocumentModel.source == document.source
                )
            ).scalar()

            version = (max_version or 0) + 1

            doc_model = DocumentModel(
                id=document.document_id,
                source=document.source,
                doc_type=document.doc_type,
                title=document.title,
                content_hash=document.content_hash,
                version=version,
            )

            session.add(doc_model)

            # 3️⃣ Persistir chunks
            for chunk, vector in zip(chunks, embeddings):
                chunk_model = DocumentChunkModel(
                    id=chunk.chunk_id,
                    document_id=document.document_id,
                    content=chunk.content,
                    source=chunk.source,
                    token_count=chunk.token_count,
                    embedding=vector,
                )
                session.add(chunk_model)

            session.commit()

        finally:
            session.close()
