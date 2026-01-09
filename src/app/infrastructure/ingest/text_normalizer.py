import re
from typing import List


class TextNormalizer:
    """
    Normalizador de texto jurídico.

    Objetivos:
    - Limpar ruído sem destruir estrutura normativa
    - Preservar artigos, incisos, parágrafos e alíneas
    - Padronizar espaçamento e quebras
    - Preparar texto para chunking semântico
    """

    ARTICLE_PATTERN = re.compile(
        r"(art\.?\s*\d+[ºo]?)",
        flags=re.IGNORECASE,
    )

    WHITESPACE_PATTERN = re.compile(r"[ \t]+")

    MULTI_NEWLINE_PATTERN = re.compile(r"\n{3,}")

    def normalize(self, text: str) -> str:
        """
        Pipeline principal de normalização.
        """
        text = self._normalize_line_breaks(text)
        text = self._remove_excess_whitespace(text)
        text = self._preserve_legal_structure(text)
        text = self._collapse_blank_lines(text)
        return text.strip()

    # -----------------------------
    # Etapas internas
    # -----------------------------

    def _normalize_line_breaks(self, text: str) -> str:
        """
        Padroniza quebras de linha.
        """
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def _remove_excess_whitespace(self, text: str) -> str:
        """
        Remove espaços excessivos sem afetar quebras.
        """
        lines = [
            self.WHITESPACE_PATTERN.sub(" ", line).strip()
            for line in text.split("\n")
        ]
        return "\n".join(lines)

    def _preserve_legal_structure(self, text: str) -> str:
        """
        Garante quebra de linha antes de artigos,
        evitando que fiquem colados em parágrafos anteriores.
        """
        text = self.ARTICLE_PATTERN.sub(r"\n\1", text)
        return text

    def _collapse_blank_lines(self, text: str) -> str:
        """
        Evita múltiplas linhas em branco.
        """
        return self.MULTI_NEWLINE_PATTERN.sub("\n\n", text)

    # -----------------------------
    # Utilitários futuros
    # -----------------------------

    def split_by_articles(self, text: str) -> List[str]:
        """
        Divide texto por artigos (útil para chunking jurídico).
        """
        parts = self.ARTICLE_PATTERN.split(text)
        chunks: List[str] = []

        buffer = ""
        for part in parts:
            if self.ARTICLE_PATTERN.match(part):
                if buffer:
                    chunks.append(buffer.strip())
                buffer = part
            else:
                buffer += " " + part

        if buffer.strip():
            chunks.append(buffer.strip())

        return chunks
