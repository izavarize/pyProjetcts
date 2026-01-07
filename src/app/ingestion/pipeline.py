from pathlib import Path

from sqlalchemy import create_engine

from app.application.ai_service import AIService
from app.core.config import settings
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.xml_loader import XMLLoader
from app.ingestion.loaders.html_loader import HTMLLoader
from app.ingestion.normalizer import LegalTextNormalizer
from app.infrastructure.rag.document_repository import DocumentRepository


class IngestionPipeline:
    def __init__(self) -> None:
        self._ai = AIService()

        self._pdf = PDFLoader()
        self._xml = XMLLoader()
        self._html = HTMLLoader()

        engine = create_engine(settings.pg_dsn)
        self._documents = DocumentRepository(engine)

    def ingest_path(self, path: Path) -> None:
        if path.is_dir():
            for file in path.iterdir():
                self.ingest_path(file)
            return

        if path.suffix.lower() == ".pdf":
            content, source = self._pdf.load(path)
        elif path.suffix.lower() == ".xml":
            content, source = self._xml.load(path)
        elif path.suffix.lower() in (".html", ".htm"):
            content, source = self._html.load(path)
        else:
            return

        content_hash = LegalTextNormalizer.hash(content)

        if self._documents.exists_by_hash(content_hash):
            print(f"[SKIP] Documento já ingerido: {source}")
            return

        self._ai.ingest_documents([(content, source)])
        self._documents.save(source, content_hash)

        print(f"[OK] Documento ingerido: {source}")
