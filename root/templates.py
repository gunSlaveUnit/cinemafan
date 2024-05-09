from fastapi import APIRouter, Request

from root.settings import templates

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="root/index.html",
    )
