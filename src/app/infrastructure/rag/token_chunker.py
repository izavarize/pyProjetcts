from collections.abc import Iterable


class TokenChunker:
    def __init__(self, chunk_tokens: int = 200, overlap_tokens: int = 40) -> None:
        if overlap_tokens >= chunk_tokens:
            raise ValueError("overlap_tokens deve ser menor que chunk_tokens")

        self.chunk_tokens = chunk_tokens
        self.overlap_tokens = overlap_tokens

    def _tokenize(self, text: str) -> list[str]:
        # Tokenização simples e determinística (proxy)
        return text.split()

    def _detokenize(self, tokens: list[str]) -> str:
        return " ".join(tokens)

    def chunk(self, text: str) -> list[str]:
        tokens = self._tokenize(text)
        chunks: list[str] = []

        start = 0
        total = len(tokens)

        while start < total:
            end = start + self.chunk_tokens
            chunk_tokens = tokens[start:end]

            if chunk_tokens:
                chunks.append(self._detokenize(chunk_tokens))

            start = end - self.overlap_tokens

        return chunks

    def chunk_many(self, texts: Iterable[str]) -> list[str]:
        all_chunks: list[str] = []
        for text in texts:
            all_chunks.extend(self.chunk(text))
        return all_chunks
