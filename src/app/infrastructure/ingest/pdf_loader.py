from pathlib import Path
import hashlib
import fitz  # PyMuPDF

from app.domain.document import Document
from app.infrastructure.ingest.base_loader import BaseLoader


class PDFLoader(BaseLoader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".pdf"

    def load(self, path: Path) -> Document:
        pdf = fitz.open(path)
        text = "\n".join(page.get_text() for page in pdf)
        normalized = text.strip()

        content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

        return Document(
            source=str(path),
            doc_type="pdf",
            title=path.stem,
            text=normalized,
            content_hash=content_hash,
            metadata={
                "file_name": path.name,
                "pages": str(len(pdf)),
            },
        )
