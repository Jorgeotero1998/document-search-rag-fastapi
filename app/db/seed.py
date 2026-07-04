from __future__ import annotations

import os

from sqlalchemy import select

from app.core.security import hash_password
from app.db.models.user import User
from app.db.session import SessionLocal


async def ensure_admin_user() -> None:
    """
    Creates an initial admin user if ADMIN_EMAIL/ADMIN_PASSWORD are set.
    Safe to call multiple times.
    """
    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "").strip()
    if not email or not password:
        return

    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()
        if existing:
            return
        user = User(email=email, hashed_password=hash_password(password), role="admin", is_active=True)
        db.add(user)
        await db.commit()

