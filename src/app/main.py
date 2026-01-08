from app.application.ai_service import AIService


def main() -> None:
    ai = AIService()

    perguntas = [
        "o que diz o art. 3º da constituição brasileira?",
        "quais são os objetivos fundamentais da república?",
        "o que significa erradicar a pobreza no contexto constitucional?",
    ]

    for pergunta in perguntas:
        result = ai.answer_with_rag(pergunta)

        print("\nPergunta:")
        print(pergunta)

        print("\nResposta:")
        print(result.answer)

        if result.sources:
            print("\nFontes:")
            for src in result.sources:
                print(f"- {src}")
        else:
            print("\nFontes:")
            print("Resposta baseada em conhecimento geral.")


if __name__ == "__main__":
    main()
