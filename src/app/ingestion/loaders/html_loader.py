from pathlib import Path

from bs4 import BeautifulSoup

from app.ingestion.normalizer import LegalTextNormalizer


class HTMLLoader:
    def load(self, path: Path) -> tuple[str, str]:
        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(separator=" ")
        normalized = LegalTextNormalizer.normalize(text)

        return normalized, path.name
