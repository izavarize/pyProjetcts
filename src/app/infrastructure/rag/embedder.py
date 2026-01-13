from abc import ABC, abstractmethod
from typing import List


class Embedder(ABC):
    """
    Contrato para qualquer mecanismo de embedding.
    """

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Recebe uma lista de textos e retorna embeddings vetoriais.
        """
        raise NotImplementedError
