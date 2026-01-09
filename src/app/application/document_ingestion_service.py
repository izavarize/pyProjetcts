from pathlib import Path
from typing import List, Optional

from app.domain.document import Document

from app.infrastructure.ingest.pdf_loader import PDFLoader
from app.infrastructure.ingest.html_loader import HTMLLoader
from app.infrastructure.ingest.xml_loader import XMLLoader


class DocumentIngestionService:
    """
    Caso de uso de ingestão de documentos jurídicos.
    Orquestra loaders de infraestrutura (filesystem / parsing).
    """

    def __init__(self):
        self._loaders = [
            PDFLoader(),
            HTMLLoader(),
            XMLLoader(),
        ]

    def ingest(
        self,
        directory: Optional[Path] = None,
        files: Optional[List[Path]] = None,
    ) -> List[Document]:

        paths: List[Path] = []

        if directory:
            paths.extend(p for p in directory.rglob("*") if p.is_file())

        if files:
            paths.extend(files)

        documents: List[Document] = []

        for path in paths:
            for loader in self._loaders:
                if loader.supports(path):
                    documents.append(loader.load(path))
                    break

        return documents
