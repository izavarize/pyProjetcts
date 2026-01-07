from pathlib import Path

from PyPDF2 import PdfReader

from app.ingestion.normalizer import LegalTextNormalizer


class PDFLoader:
    def load(self, path: Path) -> tuple[str, str]:
        reader = PdfReader(str(path))
        pages_text = []

        for page in reader.pages:
            if page.extract_text():
                pages_text.append(page.extract_text())

        full_text = "\n".join(pages_text)
        normalized = LegalTextNormalizer.normalize(full_text)

        return normalized, path.name
