from app.application.rag.rag_answer_service import RAGAnswerService
from app.infrastructure.ai.llm_stub import LLMStub


def main():
    service = RAGAnswerService(llm=LLMStub())

    result = service.answer(
        "O que dispõe o art. 3º da Constituição Federal?"
    )

    print("Resposta:")
    print(result["answer"])
    print("\nFontes:")
    for s in result["sources"]:
        print(s)


if __name__ == "__main__":
    main()
