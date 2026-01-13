from app.core.config import settings
from app.infrastructure.ai.gemini_client import GeminiClient
from app.application.rag_service import RAGService


class AIService:
    def __init__(self) -> None:
        self._llm = GeminiClient()
        self._rag = RAGService(min_score=settings.min_score)

    def answer_with_rag(self, question: str) -> str:
        retrieved = self._rag.retrieve(question)

        if retrieved:
            context = "\n\n".join(
                f"Fonte: {r.source}\n{r.content}" for r in retrieved
            )

            prompt = f"""
            Responda à pergunta com base exclusivamente no contexto abaixo.

            CONTEXTO:
            {context}

            PERGUNTA:
            {question}
            """

            return self._llm.generate(prompt)

        # fallback controlado
        prompt = f"""
        Responda de forma objetiva. Se não souber, diga explicitamente
        que a informação não consta na base consultada.

        PERGUNTA:
        {question}
        """

        return self._llm.generate(prompt)
