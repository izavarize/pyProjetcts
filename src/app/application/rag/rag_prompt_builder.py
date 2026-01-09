from typing import List, Dict


class RAGPromptBuilder:
    """
    Constrói prompt jurídico com evidências e instruções de citação.
    """

    def build(self, question: str, evidences: List[Dict]) -> str:
        context_blocks = []
        for idx, ev in enumerate(evidences, start=1):
            context_blocks.append(
                f"[Fonte {idx}] (score={ev['score']:.3f})\n{ev['content']}"
            )

        context = "\n\n".join(context_blocks)

        return f"""
Você é um assistente jurídico.
Responda APENAS com base nas fontes abaixo.
Se a resposta não estiver clara nas fontes, diga explicitamente que não há evidência suficiente.

Pergunta:
{question}

Fontes:
{context}

Instruções:
- Seja preciso e objetivo
- Cite as fontes no formato: (Fonte X)
- Não invente informações
"""
