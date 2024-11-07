from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from settings import templates
from . import models

router = APIRouter(prefix="")


@router.get("/auth/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/sign-up.html",
        context={},
    )


@router.post("/api/v1/auth/sign-up")
async def sign_up(
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
):
    user = await models.User.create({"name": name, "password": password}, db)
    