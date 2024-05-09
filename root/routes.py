from root.templates import templates

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
