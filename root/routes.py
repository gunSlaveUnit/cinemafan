from fastapi import APIRouter, Cookie, Depends, Request
import jwt

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

import uuid


from auth.models import User

from settings import ALGORITHM, SECRET_KEY, base_context, templates

router = APIRouter()


@router.get("/")
async def home(
        request: Request, 
        token: str = Cookie(None),
        db: AsyncSession = Depends(get_db),
):
    context = base_context.copy()

    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload["id"]

        user = await User.by_id(uuid.UUID(user_id), db)
        context["user"] = user

    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context=context,
    )
