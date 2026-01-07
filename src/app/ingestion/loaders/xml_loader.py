from pathlib import Path
import xml.etree.ElementTree as ET

from app.ingestion.normalizer import LegalTextNormalizer


class XMLLoader:
    def load(self, path: Path) -> tuple[str, str]:
        tree = ET.parse(path)
        root = tree.getroot()

        texts = []

        for elem in root.iter():
            if elem.text:
                texts.append(elem.text)

        full_text = "\n".join(texts)
        normalized = LegalTextNormalizer.normalize(full_text)

        return normalized, path.name
