import json
from datetime import date

from app.application.rag_service import RAGService
from app.core.config import settings
from app.domain.rag import DocumentChunk
from app.domain.rag_response import RAGAnswer
from app.infrastructure.ai.gemini_client import GeminiClient


class AIService:
    def __init__(self) -> None:
        self._llm = GeminiClient(
            api_key=settings.google_api_key,
            model=settings.gemini_model,
        )
        self._rag = RAGService()

    def ingest_documents(self, docs: list[tuple[str, str]]) -> None:
        chunks = [
            DocumentChunk(content=content, source=source)
            for content, source in docs
        ]
        self._rag.ingest(chunks)

    def answer_with_rag(self, question: str) -> RAGAnswer:
        retrieved = self._rag.retrieve(question)

        if not retrieved:
            return self._fallback_answer(question)

        context_blocks = []
        sources = []

        for chunk in retrieved:
            context_blocks.append(
                f"[Fonte: {chunk.source}]\n{chunk.content}"
            )
            sources.append(chunk.source)

        context = "\n\n".join(context_blocks)

        prompt = f"""
Responda à pergunta utilizando EXCLUSIVAMENTE as informações do contexto abaixo.

Contexto:
{context}

Pergunta:
{question}

Retorne a resposta no seguinte JSON:
{{"answer": string, "sources": string[]}}
"""

        raw = self._llm.generate(prompt)
        cleaned = self._extract_json(raw)
        data = json.loads(cleaned)

        return RAGAnswer.model_validate(data)

    def _fallback_answer(self, question: str) -> RAGAnswer:
        today = date.today().strftime("%d/%m/%Y")

        prompt = f"""
Você é um assistente jurídico.

A pergunta abaixo não possui base documental.
Responda com conhecimento geral e ressalva explícita.

Data atual: {today}

Pergunta:
{question}

Retorne JSON:
{{"answer": string, "sources": []}}
"""

        raw = self._llm.generate(prompt)
        cleaned = self._extract_json(raw)
        data = json.loads(cleaned)

        return RAGAnswer.model_validate(data)

    @staticmethod
    def _extract_json(text: str) -> str:
        text = text.strip()

        if text.startswith("```"):
            text = text.split("```", 1)[1]
            text = text.rsplit("```", 1)[0]

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise RuntimeError("JSON não encontrado")

        return text[start : end + 1]
