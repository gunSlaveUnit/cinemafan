"""Sign up / in / out API routes and templates."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
)
from fastapi.responses import RedirectResponse
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from db import get_db
from settings import ALGORITHM, SECRET_KEY, templates
from shared.utils import fill_base_context

router = APIRouter(prefix="")


@router.post("/api/v1/auth/sign-up")
async def sign_up(
        email: Annotated[str, Form()],
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """Creates user account.

    Args:
        email (str): New user email.
        name (str): New user name.
        password (str): New user password.
        db (AsyncSession): Database session.

    Returns:
        RedirectResponse: Redirects to sign in page.
    """

    _: User = await User.create(
        {
            "email": email, 
            "name": name,
            "password": password,
        },
        db,
    )

    return RedirectResponse("/auth/sign-in", status_code=303)


@router.post("/api/v1/auth/sign-in")
async def sign_in(
        name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """Authorizes the user in the system
    by storing the access token in a cookie.

    Args:
        name (str): User name.
        password (str): User password.
        db (AsyncSession): Database session.

    Returns:
        RedirectResponse: Redirects to the home page.
    """

    user = await User.by_name(name, db)

    if user and user.password == password:
        token = jwt.encode(
            {"id": str(user.id)},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        response = RedirectResponse("/", status_code=303)
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
        )

        return response
    else:
        print("not found")


@router.get("/auth/sign-up")
async def sign_up_page(
        request: Request,
        base_context: dict = Depends(fill_base_context),
) -> templates.TemplateResponse:
    """Page to create a new user account.

    Args:
        request (Request): FastAPI request.
        base_context (dict): Context with common page data.

    Returns:
        templates.TemplateResponse: Sign up template with mapped context.
    """

    return templates.TemplateResponse(
        request=request,
        name="auth/sign-up.html",
        context=base_context,
    )


@router.get("/auth/sign-in")
async def sign_in_page(
        request: Request,
        base_context: dict = Depends(fill_base_context),
) -> templates.TemplateResponse:
    """Page to sign in to the system.

    Args:
        request (Request): FastAPI request.
        base_context (dict): Context with common page data.

    Returns:
        templates.TemplateResponse: Sign in template with mapped context.
    """

    return templates.TemplateResponse(
        request=request,
        name="auth/sign-in.html",
        context=base_context,
    )


@router.post("/auth/sign-out")
async def sign_out(request: Request) -> RedirectResponse:
    """Logs the user out by removing the access token from the cookie.

    Args:
        request (Request): FastAPI request.

    Returns:
        RedirectResponse: Redirects to the home page.
    """

    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(key="token")
    return response
