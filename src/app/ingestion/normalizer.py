import hashlib
import re


class LegalTextNormalizer:
    """
    Normaliza texto jurídico e gera hash criptográfico.
    """

    @staticmethod
    def normalize(text: str) -> str:
        text = text.replace("\u00a0", " ")
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        # Padronizações jurídicas
        text = text.replace("Art.", "Artigo")
        text = text.replace("§", "Parágrafo")
        text = text.replace("Inc.", "Inciso")

        return text

    @staticmethod
    def hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
