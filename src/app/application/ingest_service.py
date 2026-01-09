from datetime import datetime
from app.application.rag_service import RAGService
from app.domain.telemetry import TelemetryEvent


class AIService:
    def __init__(self, llm, rag: RAGService, telemetry_repo):
        self._llm = llm
        self._rag = rag
        self._telemetry = telemetry_repo

    def answer_with_rag(self, question: str):
        start = datetime.utcnow()

        retrieved, rag_metrics = self._rag.retrieve(question)

        if not retrieved:
            answer = self._llm.generate(question)
            rag_metrics["used_fallback"] = True
        else:
            context = "\n\n".join(r.content for r in retrieved)
            prompt = f"Contexto:\n{context}\n\nPergunta:\n{question}"
            answer = self._llm.generate(prompt)

        duration_ms = (datetime.utcnow() - start).total_seconds() * 1000

        event = TelemetryEvent(
            timestamp=datetime.utcnow(),
            operation="answer_with_rag",
            duration_ms=duration_ms,
            success=True,
            retrieved_chunks=rag_metrics["retrieved_chunks"],
            max_score=rag_metrics["max_score"],
            avg_score=rag_metrics["avg_score"],
            min_score=rag_metrics["min_score"],
            coverage=rag_metrics["coverage"],
            used_fallback=rag_metrics["used_fallback"],
        )

        self._telemetry.save(event)

        return answer
