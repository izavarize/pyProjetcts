from collections.abc import Iterable


class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 100) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap deve ser menor que chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []

        chunks: list[str] = []
        start = 0
        length = len(text)

        while start < length:
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.overlap

        return chunks

    def chunk_many(self, texts: Iterable[str]) -> list[str]:
        all_chunks: list[str] = []
        for text in texts:
            all_chunks.extend(self.chunk(text))
        return all_chunks
