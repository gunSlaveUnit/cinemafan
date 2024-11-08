import uuid
from typing import Awaitable

from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from db import get_db
from settings import ALGORITHM, SECRET_KEY
from auth.models import User


async def get_current_user(
    token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> Awaitable[User | None]:
    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await User.by_id(uuid.UUID(payload["id"]), db)
    return None