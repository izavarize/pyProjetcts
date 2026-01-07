import json
from app.core.config import settings
from app.domain.ai_responses import CodeExplanation
from app.infrastructure.ai.gemini_client import GeminiClient
from app.application.rag_service import RAGService
from app.domain.rag import DocumentChunk


class AIService:
    def __init__(self) -> None:
        self._llm = GeminiClient(
            api_key=settings.google_api_key,
            model=settings.gemini_model,
        )

    def explain_code(self, code: str) -> CodeExplanation:
        prompt = f"""
Analise o código abaixo e responda EXCLUSIVAMENTE em JSON válido,
SEM blocos markdown, SEM ```json, seguindo exatamente este schema:

{{
  "summary": string,
  "inputs": string[],
  "output": string,
  "language": string
}}

Código:
{code}
"""
        raw_response = self._llm.generate(prompt)

        cleaned = self._extract_json(raw_response)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Resposta da IA não é um JSON válido.\n"
                f"Resposta bruta:\n{raw_response}"
            ) from exc

        return CodeExplanation.model_validate(data)

    @staticmethod
    def _extract_json(text: str) -> str:
        """
        Extrai o primeiro objeto JSON válido de uma resposta de LLM,
        ignorando markdown, texto extra ou caracteres inválidos.
        """
        text = text.strip()

        # Remove blocos markdown se existirem
        if text.startswith("```"):
            text = text.split("```", 1)[1]
            text = text.rsplit("```", 1)[0]

        # Localiza o primeiro e o último delimitador JSON
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise RuntimeError(f"Não foi possível extrair JSON da resposta:\n{text}")

        return text[start : end + 1]


class AIService:
    def __init__(self) -> None:
        self._llm = GeminiClient(
            api_key=settings.google_api_key,
            model=settings.gemini_model,
        )
        self._rag = RAGService()

    def ingest_documents(self, docs: list[tuple[str, str]]) -> None:
        chunks = [
            DocumentChunk(content=content, source=source) for content, source in docs
        ]
        self._rag.ingest(chunks)

    def answer_with_rag(self, question: str) -> str:
        retrieved = self._rag.retrieve(question)

        context = "\n\n".join(f"Fonte: {c.source}\n{c.content}" for c in retrieved)

        prompt = f"""
Use exclusivamente o contexto abaixo para responder à pergunta.
Contexto:
{context}
Pergunta:
{question}
"""

        return self._llm.generate(prompt)
