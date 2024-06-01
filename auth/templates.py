from fastapi import APIRouter, Request

from infrastructure.settings import templates

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse(
        context={},
        name="auth/sign-up.html",
        request=request,
    )


@router.get("/sign-in")
async def sign_in(request: Request):
    return templates.TemplateResponse(
        context={},
        name="auth/sign-in.html",
        request=request,
    )
