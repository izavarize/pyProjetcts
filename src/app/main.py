from app.application.ai_service import AIService


def main() -> None:
    ai = AIService()

    ai.ingest_documents(
        [
            (
                "A função soma recebe dois parâmetros e retorna a soma.",
                "manual-python.txt",
            ),
            (
                "Em Python, funções são definidas com a palavra-chave def.",
                "doc-python.txt",
            ),
        ]
    )

    answer = ai.answer_with_rag("Como funciona a função soma?")
    print(answer)


if __name__ == "__main__":
    main()
