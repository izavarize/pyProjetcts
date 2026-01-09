from typing import List, Dict
from app.domain.document import Document
from app.domain.document_chunk import DocumentChunk
from app.infrastructure.ingest.text_normalizer import TextNormalizer


class JuridicalChunker:
    """
    Chunker jurídico híbrido:
    - Prioriza estrutura legal (artigos/parágrafos)
    - Aplica tokenização quando necessário
    """

    def __init__(self, max_tokens: int = 400, overlap: int = 50):
        self._max_tokens = max_tokens
        self._overlap = overlap
        self._normalizer = TextNormalizer()

    # -----------------------------
    # API pública
    # -----------------------------

    def chunk(self, document: Document) -> List[DocumentChunk]:
        """
        Gera chunks jurídicos a partir de um documento normalizado.
        """
        normalized_text = self._normalizer.normalize(document.text)

        # 1) Divide por artigos
        article_blocks = self._normalizer.split_by_articles(normalized_text)

        chunks: List[DocumentChunk] = []

        for block in article_blocks:
            tokens = self._tokenize(block)

            if len(tokens) <= self._max_tokens:
                chunks.append(self._build_chunk(document, block, tokens))
            else:
                sub_chunks = self._chunk_by_tokens(tokens)
                for sub in sub_chunks:
                    chunks.append(self._build_chunk(document, sub, self._tokenize(sub)))

        return chunks

    # -----------------------------
    # Internos
    # -----------------------------

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenização simples (agnóstica de modelo).
        Substituível futuramente por tokenizer específico.
        """
        return text.split()

    def _chunk_by_tokens(self, tokens: List[str]) -> List[str]:
        """
        Divide tokens respeitando tamanho máximo e overlap.
        """
        chunks: List[str] = []
        start = 0

        while start < len(tokens):
            end = start + self._max_tokens
            slice_tokens = tokens[start:end]
            chunks.append(" ".join(slice_tokens))

            start = end - self._overlap
            if start < 0:
                start = 0

        return chunks

    def _build_chunk(
        self,
        document: Document,
        content: str,
        tokens: List[str],
    ) -> DocumentChunk:
        """
        Constrói um DocumentChunk com metadados jurídicos.
        """
        metadata: Dict[str, str] = {
            "doc_type": document.doc_type,
            "source": document.source,
        }

        # Heurística simples para capturar artigo
        lowered = content.lower()
        if lowered.startswith("art"):
            first_line = content.split("\n", 1)[0]
            metadata["article"] = first_line.strip()

        return DocumentChunk(
            document_id=document.document_id,
            content=content.strip(),
            source=document.source,
            metadata=metadata,
            token_count=len(tokens),
        )
