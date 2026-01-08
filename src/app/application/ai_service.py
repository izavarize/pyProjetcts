from app.core.config import settings
from app.domain.answer import AnswerResult
from app.application.rag_service import RAGService
from app.infrastructure.ai.gemini_client import GeminiClient
from app.infrastructure.ai.llm_client import LLMClient


class AIService:
    def __init__(self) -> None:
        self._rag = RAGService()

        # 🔑 Aqui está a correção
        self._llm: LLMClient = GeminiClient(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )

    def answer_with_rag(self, question: str) -> AnswerResult:
        retrieved = self._rag.retrieve(question)

        if not retrieved:
            return self._fallback_answer(question)

        context = "\n\n".join(chunk.content for chunk in retrieved)

        prompt = f"""
Você é um assistente jurídico.
Use EXCLUSIVAMENTE o contexto abaixo para responder à pergunta.

CONTEXTO:
{context}

PERGUNTA:
{question}

Responda em texto claro e objetivo.
"""

        raw = self._llm.generate(prompt)

        return AnswerResult(
            answer=raw,
            sources=[c.source for c in retrieved],
        )

    def _fallback_answer(self, question: str) -> AnswerResult:
        prompt = f"""
Você é um assistente jurídico.
Responda à pergunta abaixo de forma clara e objetiva.

PERGUNTA:
{question}
"""

        raw = self._llm.generate(prompt)

        return AnswerResult(
            answer=raw,
            sources=[],
        )
