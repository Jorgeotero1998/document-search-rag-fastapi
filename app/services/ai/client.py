from __future__ import annotations

from dataclasses import dataclass

from openai import AsyncOpenAI

from app.core.config import settings


@dataclass(frozen=True)
class AIMessage:
    role: str
    content: str


class AIClient:
    def __init__(self) -> None:
        base_url = str(settings.llm_base_url) if settings.llm_base_url else None
        self._client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=base_url)

    async def chat(self, *, messages: list[AIMessage]) -> str:
        resp = await self._client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=0.2,
        )
        return (resp.choices[0].message.content or "").strip()


def get_ai_client() -> AIClient:
    return AIClient()

