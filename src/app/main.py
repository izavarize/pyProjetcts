from app.application.ai_service import AIService


def main() -> None:
    ai = AIService()

    ai.ingest_documents(
        [
            (
                "A função soma recebe dois parâmetros e retorna a soma. "
                "Ela é usada para operações matemáticas simples em Python. "
                "Funções em Python são definidas com a palavra-chave def.",
                "manual-python.txt",
            ),
        ]
    )

    answer = ai.answer_with_rag("Como funciona a função soma?")
    print(answer)


if __name__ == "__main__":
    main()
