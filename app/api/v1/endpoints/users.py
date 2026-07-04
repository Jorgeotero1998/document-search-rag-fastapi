from __future__ import annotations

from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.api.v1.deps import get_db, require_roles
from app.core.security import hash_password
from app.db.models.user import User

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"


class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: str
    is_active: bool


@router.get("", response_model=list[UserOut])
async def list_users(db=Depends(get_db), _: User = Depends(require_roles("admin"))):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [
        UserOut(id=str(u.id), email=u.email, role=u.role, is_active=u.is_active) for u in users
    ]


@router.post("", response_model=UserOut)
async def create_user(payload: UserCreate, db=Depends(get_db), _: User = Depends(require_roles("admin"))):
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut(id=str(user.id), email=user.email, role=user.role, is_active=user.is_active)

