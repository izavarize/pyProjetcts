from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Gera texto a partir de um prompt.
        """
        raise NotImplementedError
