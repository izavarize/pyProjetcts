import hashlib
import json

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.ask import AskRequest, AskResponse, SourceItem
from app.api.deps import get_ai_service
from app.application.ai_service import AIService
from app.infrastructure.cache.memory_cache import MemoryCache

router = APIRouter(prefix="/ask", tags=["Ask"])

_cache = MemoryCache(ttl_seconds=300)


def _hash_question(question: str) -> str:
    return hashlib.sha256(question.strip().lower().encode()).hexdigest()


@router.post("", response_model=AskResponse)
def ask(
    payload: AskRequest,
    ai: AIService = Depends(get_ai_service),
):
    key = _hash_question(payload.question)

    cached = _cache.get(key)
    if cached:
        return cached

    try:
        retrieved = ai._rag.retrieve(payload.question)
        answer = ai.answer_with_rag(payload.question)

        response = AskResponse(
            answer=answer,
            sources=[
                SourceItem(source=r.source, score=round(r.score, 3))
                for r in retrieved
            ],
            used_rag=bool(retrieved),
        )

        # só cacheia se a resposta for fundamentada
        if response.used_rag:
            _cache.set(key, response)

        return response

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
