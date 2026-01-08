from typing import List

from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """
    Gera embeddings localmente (sem custo / sem quota).
    """

    def __init__(self) -> None:
        # Modelo leve, rápido e excelente para RAG
        self._model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
