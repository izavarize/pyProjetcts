class AnswerValidator:
    """
    Valida se a resposta segue as diretrizes jurídicas.
    """

    @staticmethod
    def is_valid(answer: str) -> bool:
        lowered = answer.lower()

        # resposta negativa padrão
        if "não foi possível responder" in lowered:
            return True

        # exige algum indicativo de fonte
        indicators = [
            "art.",
            "artigo",
            "lei",
            "constituição",
            "fonte",
            "nota técnica",
            "instrução normativa",
            "ajuste sinief",
            "portaria",
            "comunicado técnico"
        ]

        return any(i in lowered for i in indicators)
