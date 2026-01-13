from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Contrato único para qualquer LLM (Gemini, OpenAI, etc).
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Gera texto a partir de um prompt.
        """
        raise NotImplementedError
