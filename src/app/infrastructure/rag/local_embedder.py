from typing import List
from sentence_transformers import SentenceTransformer

from app.infrastructure.rag.embedder import Embedder


class LocalEmbedder(Embedder):
    def __init__(self) -> None:
        self._model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return embeddings.tolist()
