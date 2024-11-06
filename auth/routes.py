from fastapi import APIRouter, Request

from settings import templates

router = APIRouter(prefix="")


@router.get("/auth/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/sign-up.html",
        context={},
    )