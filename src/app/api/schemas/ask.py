from pydantic import BaseModel, Field
from typing import List


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)
    mode: str = Field(default="strict", description="strict | interpretative")


class SourceItem(BaseModel):
    source: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    used_rag: bool
