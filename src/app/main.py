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

    result = ai.answer_with_rag("o que diz o art. 3º da constituição brasileira?")

    print("Resposta:")
    print(result.answer)

    print("\nFontes:")
    for src in result.sources:
        print(f"- {src}")


if __name__ == "__main__":
    main()
