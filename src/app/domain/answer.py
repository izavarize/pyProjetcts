from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AnswerResult:
    """
    Resultado final de uma resposta do sistema.
    """

    answer: str
    sources: List[str]
