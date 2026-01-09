from pathlib import Path
import hashlib
from lxml import etree

from app.domain.document import Document
from app.infrastructure.ingest.base_loader import BaseLoader


class XMLLoader(BaseLoader):
    def supports(self, path: Path) -> bool:
        return path.suffix.lower() == ".xml"

    def load(self, path: Path) -> Document:
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(str(path), parser)

        text_nodes = tree.xpath("//text()")
        text = "\n".join(t.strip() for t in text_nodes if t.strip())
        normalized = text.strip()

        content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

        return Document(
            source=str(path),
            doc_type="xml",
            title=path.stem,
            text=normalized,
            content_hash=content_hash,
            metadata={
                "file_name": path.name,
            },
        )
