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
        """
        Recebe documentos brutos e delega a ingestão ao RAG.
        """
        chunks = [
            DocumentChunk(content=content, source=source) for content, source in docs
        ]
        self._rag.ingest(chunks)

    def answer_with_rag(self, question: str) -> RAGAnswer:
        """
        Primeiro tenta responder via RAG.
        Se não houver contexto relevante, faz fallback para LLM puro.
        """
        retrieved = self._rag.retrieve(question)

        if not retrieved:
            return self._fallback_answer(question)

        context_blocks = []
        sources = []

        for chunk in retrieved:
            context_blocks.append(f"[Fonte: {chunk.source}]\n{chunk.content}")
            sources.append(chunk.source)

        context = "\n\n".join(context_blocks)

        prompt = f"""
Responda à pergunta utilizando EXCLUSIVAMENTE as informações do contexto abaixo.

Contexto:
{context}

Pergunta:
{question}

Instruções obrigatórias:
- Não invente informações.
- Se a resposta não estiver no contexto, diga que não foi encontrada.
- Retorne a resposta no seguinte JSON:

{{
  "answer": string,
  "sources": string[]
}}
"""

        raw = self._llm.generate(prompt)
        cleaned = self._extract_json(raw)
        data = json.loads(cleaned)

        return RAGAnswer.model_validate(data)

    def _fallback_answer(self, question: str) -> RAGAnswer:
        """
        Fallback para LLM puro quando o RAG não encontra contexto.
        """
        today = date.today().strftime("%d/%m/%Y")

        prompt = f"""
Você é um assistente jurídico e informacional.

A pergunta abaixo NÃO possui base nos documentos fornecidos.
Responda com base em conhecimento geral, deixando claro que
a resposta NÃO está fundamentada em documentos específicos.

Data atual: {today}

Pergunta:
{question}

Retorne a resposta no seguinte JSON:

{{
  "answer": string,
  "sources": []
}}
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

        if start == -1 or end == -1 or end <= start:
            raise RuntimeError(f"JSON não encontrado na resposta:\n{text}")

        return text[start : end + 1]
