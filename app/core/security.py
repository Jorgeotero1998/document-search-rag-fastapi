from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def _encode(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def _decode(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])


def create_access_token(*, sub: str, role: str) -> str:
    now = int(time.time())
    exp = now + settings.jwt_access_ttl_seconds
    return _encode({"typ": "access", "sub": sub, "role": role, "iat": now, "exp": exp})


def create_refresh_token(*, sub: str) -> str:
    now = int(time.time())
    exp = now + settings.jwt_refresh_ttl_seconds
    return _encode({"typ": "refresh", "sub": sub, "iat": now, "exp": exp})


def decode_token(token: str) -> dict[str, Any]:
    try:
        return _decode(token)
    except JWTError as e:
        raise ValueError("Invalid token") from e

