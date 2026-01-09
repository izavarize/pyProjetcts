from typing import List
from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """
    Embedder local baseado em Sentence-Transformers.
    Determinístico, sem quota, compatível com pgvector.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self._model = SentenceTransformer(model_name)
        self.dimension = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Gera embeddings normalizados (cosine-ready).
        """
        vectors = self._model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vectors.tolist()
