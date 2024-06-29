from fastapi import APIRouter, Request

from infrastructure.settings import templates

router = APIRouter()

@router.get("/auth/sign-up")
async def sign_up_page(request: Request):
    return templates.TemplateResponse(
        context={},
        name="auth/sign-up.html",
        request=request,
    )


@router.get("/auth/sign-in")
async def sign_in_page(request: Request):
    return templates.TemplateResponse(
        context={},
        name="auth/sign-in.html",
        request=request,
    )


@router.post("/api/auth/sign-up")
async def sign_up() -> None:
    pass


@router.post("/api/auth/sign-in")
async def sign_in() -> None:
    pass


@router.post("/api/auth/sign-out")
async def sign_out() -> None:
    pass
