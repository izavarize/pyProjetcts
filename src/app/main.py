from app.application.ai_service import AIService


def main() -> None:
    ai_service = AIService()

    code_example = """
def soma(a, b):
    return a + b
"""

    explanation = ai_service.explain_code(code_example)

    print("Resposta do Gemini:")
    print(explanation)


if __name__ == "__main__":
    main()
