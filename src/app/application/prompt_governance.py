from typing import List

from app.domain.rag import DocumentChunk


class PromptGovernance:
    """
    Centraliza as regras jurídicas de resposta.
    """

    @staticmethod
    def build_rag_prompt(
        question: str,
        context_chunks: List[DocumentChunk],
    ) -> str:
        context = "\n\n".join(
            f"FONTE: {c.source}\nTEXTO:\n{c.content}"
            for c in context_chunks
        )

        return f"""
Você é um assistente jurídico.

REGRAS OBRIGATÓRIAS:
1. Responda APENAS com base no CONTEXTO fornecido.
2. Cite explicitamente a fonte utilizada (ex: artigo, lei, documento).
3. NÃO presuma, NÃO complete lacunas, NÃO use conhecimento externo.
4. Se a resposta NÃO estiver claramente fundamentada no contexto,
   responda exatamente:
   "Não foi possível responder com base nos documentos fornecidos."

CONTEXTO:
{context}

PERGUNTA:
{question}

FORMATO DA RESPOSTA:
- Resposta objetiva
- Citação explícita da fonte
"""
