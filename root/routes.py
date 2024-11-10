import datetime

from fastapi import APIRouter, Cookie, Depends, Request
import jwt

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db

import uuid


from auth.models import User

from settings import ALGORITHM, SECRET_KEY, base_context, templates

router = APIRouter()

from shared.utils import get_current_user


@router.get("/")
async def home(
        request: Request,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    context = base_context.copy()
    context["current_year"] = datetime.datetime.now().year
    context["user"] = current_user

    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context=context,
    )
