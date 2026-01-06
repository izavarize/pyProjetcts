from app.application.ai_service import AIService


def main() -> None:
    ai = AIService()

    result = ai.explain_code(
        """
def soma(a, b):
    return a + b
"""
    )

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
