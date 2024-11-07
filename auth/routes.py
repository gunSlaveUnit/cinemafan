from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from settings import templates
from . import models

router = APIRouter(prefix="")


@router.get("/auth/sign-up")
async def sign_up_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/sign-up.html",
    )


@router.post("/api/v1/auth/sign-up")
async def sign_up(
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
):
    user = await models.User.create({"name": name, "password": password}, db)
    return RedirectResponse("/auth/sign-in", status_code=303)


@router.get("/auth/sign-in")
async def sign_in_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/sign-in.html",
    )


@router.post("/api/v1/auth/sign-in")
async def sign_in(
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
):
    user = await models.User.by_name(name, db)
    if user and user.password == password:
        return RedirectResponse("/", status_code=303)
    else:
        print("not found")
