from pathlib import Path
import hashlib
from bs4 import BeautifulSoup

from app.domain.document import Document
from app.infrastructure.ingest.base_loader import BaseLoader


class HTMLLoader(BaseLoader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in {".html", ".htm"}

    def load(self, path: Path) -> Document:
        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        normalized = text.strip()

        content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

        return Document(
            source=str(path),
            doc_type="html",
            title=soup.title.string if soup.title else path.stem,
            text=normalized,
            content_hash=content_hash,
            metadata={
                "file_name": path.name,
            },
        )
