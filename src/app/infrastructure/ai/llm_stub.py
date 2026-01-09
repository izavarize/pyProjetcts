from app.application.interfaces.llm_client import LLMClient


class LLMStub(LLMClient):
    def generate(self, prompt: str) -> str:
        return "Resposta simulada baseada nas fontes fornecidas."
