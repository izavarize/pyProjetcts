from pydantic import BaseModel, Field


class CodeExplanation(BaseModel):
    summary: str = Field(..., description="Resumo curto do código")
    inputs: list[str] = Field(..., description="Parâmetros de entrada")
    output: str = Field(..., description="Descrição do retorno")
    language: str = Field(..., description="Linguagem do código")
