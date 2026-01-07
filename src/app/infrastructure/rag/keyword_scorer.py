import re


class KeywordScorer:
    def score(self, query: str, text: str) -> float:
        """
        Score simples baseado em ocorrência de termos.
        Retorna valor entre 0.0 e 1.0
        """
        query_terms = self._normalize(query)
        text_terms = self._normalize(text)

        if not query_terms:
            return 0.0

        matches = sum(1 for term in query_terms if term in text_terms)
        return matches / len(query_terms)

    @staticmethod
    def _normalize(text: str) -> set[str]:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return {t for t in text.split() if len(t) > 2}
