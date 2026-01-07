from pydantic import BaseModel, Field


class RAGAnswer(BaseModel):
    answer: str = Field(..., description="Resposta gerada pela IA")
    sources: list[str] = Field(
        ..., description="Lista de fontes utilizadas na resposta"
    )
