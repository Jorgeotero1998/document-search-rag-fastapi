from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select

from app.api.v1.deps import get_current_user, get_db
from app.core.config import settings
from app.db.models.search import Document
from app.services.ai.client import AIMessage, get_ai_client

router = APIRouter()


class DocumentCreate(BaseModel):
    title: str
    content: str


class DocumentOut(BaseModel):
    id: str
    title: str


class SearchResponse(BaseModel):
    results: list[DocumentOut]


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    citations: list[DocumentOut]


@router.post("/docs", response_model=DocumentOut)
async def create_doc(payload: DocumentCreate, db=Depends(get_db), _=Depends(get_current_user)):
    doc = Document(title=payload.title, content=payload.content)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return DocumentOut(id=str(doc.id), title=doc.title)


@router.get("/docs/search", response_model=SearchResponse)
async def search(q: str, db=Depends(get_db), _=Depends(get_current_user)):
    if not q.strip():
        return SearchResponse(results=[])

    query = (
        select(Document)
        .where(
            func.to_tsvector("simple", Document.content).op("@@")(func.plainto_tsquery("simple", q))
        )
        .order_by(Document.created_at.desc())
        .limit(10)
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    return SearchResponse(results=[DocumentOut(id=str(d.id), title=d.title) for d in rows])


@router.post("/docs/ask", response_model=AskResponse)
async def ask(payload: AskRequest, db=Depends(get_db), _=Depends(get_current_user)):
    if not settings.llm_enabled:
        raise HTTPException(status_code=503, detail="AI disabled")

    # naive retrieval: latest docs, then ask LLM with citations
    result = await db.execute(select(Document).order_by(Document.created_at.desc()).limit(5))
    docs = result.scalars().all()
    citations = [DocumentOut(id=str(d.id), title=d.title) for d in docs]

    context = "\n\n".join([f"[{i+1}] {d.title}\n{d.content}" for i, d in enumerate(docs)])
    prompt = (
        "Answer using ONLY the provided documents. If not found, say you don't know.\n\n"
        f"Documents:\n{context}\n\nQuestion: {payload.question}\n"
        "Return a concise answer and mention citations like [1], [2]."
    )

    client = get_ai_client()
    answer = await client.chat(messages=[AIMessage(role="user", content=prompt)])
    return AskResponse(answer=answer, citations=citations)

