from typing import Dict, List

from app.application.interfaces.llm_client import LLMClient
from app.application.rag.rag_retriever import RAGRetriever
from app.application.rag.rag_prompt_builder import RAGPromptBuilder
from app.infrastructure.embeddings.local_embedder import LocalEmbedder


class RAGAnswerService:
    """
    Orquestra RAG completo com citação explícita.
    """

    def __init__(self, llm: LLMClient):
        self._embedder = LocalEmbedder()
        self._retriever = RAGRetriever()
        self._prompt_builder = RAGPromptBuilder()
        self._llm = llm

    def answer(self, question: str) -> Dict:
        query_vec = self._embedder.embed([question])[0]
        evidences = self._retriever.retrieve(query_vec)

        if not evidences:
            return {
                "answer": "Não há evidências suficientes nos documentos ingeridos.",
                "sources": [],
            }

        prompt = self._prompt_builder.build(question, evidences)
        answer_text = self._llm.generate(prompt)

        return {
            "answer": answer_text,
            "sources": [
                {
                    "source": e["source"],
                    "version": e["version"],
                    "score": e["score"],
                }
                for e in evidences
            ],
        }
