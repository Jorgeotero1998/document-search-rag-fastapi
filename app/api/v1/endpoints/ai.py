from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.config import settings
from app.services.ai.client import AIMessage, get_ai_client

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    provider: str
    model: str


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    if not settings.llm_enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI is disabled. Set LLM_ENABLED=true and configure LLM_* env vars.",
        )
    if not settings.llm_api_key:
        raise HTTPException(status_code=503, detail="Missing LLM_API_KEY")

    client = get_ai_client()
    reply = await client.chat(
        messages=[
            AIMessage(role="system", content="You are a helpful assistant inside a demo API."),
            AIMessage(role="user", content=payload.message),
        ]
    )
    return ChatResponse(reply=reply, provider=settings.llm_provider, model=settings.llm_model)

