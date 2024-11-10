import datetime
from typing import Awaitable
import uuid

from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from db import get_db
from settings import ALGORITHM, base_context, SECRET_KEY
from auth.models import User


async def get_current_user(
    token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> Awaitable[User | None]:
    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await User.by_id(uuid.UUID(payload["id"]), db)
    return None


async def fill_base_context(
        current_user: User = Depends(get_current_user), 
        db: AsyncSession = Depends(get_db),
):
    context = base_context.copy()
    context["current_year"] = datetime.datetime.now().year
    context["user"] = current_user

    return context
