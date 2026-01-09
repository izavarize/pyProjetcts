from pathlib import Path
from typing import List, Optional

from app.domain.document import Document
from app.domain.document_chunk import DocumentChunk

from app.application.document_ingestion_service import DocumentIngestionService
from app.application.chunking.juridical_chunker import JuridicalChunker
from app.application.persistence.ingestion_persistence_service import (
    IngestionPersistenceService,
)

from app.infrastructure.ingest.text_normalizer import TextNormalizer
from app.infrastructure.embeddings.local_embedder import LocalEmbedder


class FullIngestionPipeline:
    """
    Pipeline completo de ingestão jurídica:
    - Ingestão de arquivos
    - Normalização
    - Deduplicação + versionamento
    - Chunking híbrido
    - Embeddings locais
    - Persistência no Postgres (pgvector)
    """

    def __init__(self):
        self._ingestor = DocumentIngestionService()
        self._normalizer = TextNormalizer()
        self._chunker = JuridicalChunker()
        self._embedder = LocalEmbedder()
        self._persistence = IngestionPersistenceService()

        # Segurança: garantir compatibilidade com o banco
        if self._embedder.dimension != 384:
            raise RuntimeError(
                f"Dimensão de embedding incompatível: {self._embedder.dimension} != 384"
            )

    def ingest(
        self,
        directory: Optional[Path] = None,
        files: Optional[List[Path]] = None,
    ) -> None:

        documents: List[Document] = self._ingestor.ingest(
            directory=directory,
            files=files,
        )

        for document in documents:
            # 1️⃣ Normalização
            document.text = self._normalizer.normalize(document.text)

            # 2️⃣ Chunking jurídico híbrido
            chunks: List[DocumentChunk] = self._chunker.chunk(document)

            if not chunks:
                continue

            # 3️⃣ Embeddings
            contents = [c.content for c in chunks]
            embeddings = self._embedder.embed(contents)

            # 4️⃣ Persistência versionada
            self._persistence.persist(
                document=document,
                chunks=chunks,
                embeddings=embeddings,
            )
