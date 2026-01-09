from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from app.domain.document import Document


class BaseLoader(ABC):
    """
    Loader base para documentos jurídicos.
    Infraestrutura de ingestão (filesystem / parsing).
    """

    @abstractmethod
    def supports(self, path: Path) -> bool:
        pass

    @abstractmethod
    def load(self, path: Path) -> Document:
        pass

    def load_many(self, paths: List[Path]) -> List[Document]:
        documents = []
        for path in paths:
            if self.supports(path):
                documents.append(self.load(path))
        return documents
