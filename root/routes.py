from fastapi import APIRouter, Request

from settings import templates

router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
    )
