from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from db import get_db
from settings import ALGORITHM, SECRET_KEY, templates
from shared.utils import fill_base_context

router = APIRouter(prefix="")


@router.get("/auth/sign-up")
async def sign_up_page(
        request: Request,
        base_context: dict = Depends(fill_base_context),
):
    return templates.TemplateResponse(
        request=request,
        name="auth/sign-up.html",
        context=base_context,
    )


@router.post("/api/v1/auth/sign-up")
async def sign_up(
        email: Annotated[str, Form()],
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
):
    _: User = await User.create({"email": email, "name": name, "password": password}, db)
    return RedirectResponse("/auth/sign-in", status_code=303)


@router.get("/auth/sign-in")
async def sign_in_page(
        request: Request,
        base_context: dict = Depends(fill_base_context),
):
    return templates.TemplateResponse(
        request=request,
        name="auth/sign-in.html",
        context=base_context,
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/api/v1/auth/sign-in")
async def sign_in(
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
):
    user = await User.by_name(name, db)
    if user and user.password == password:
        access_token = create_access_token(data={"id": str(user.id)})

        response = RedirectResponse("/", status_code=303)
        response.set_cookie(key="token", value=access_token, httponly=True)
        return response
    else:
        print("not found")



@router.post("/auth/sign-out")
async def sign_out(
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(key="token")
    return response
