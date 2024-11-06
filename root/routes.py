from fastapi import APIRouter, Request

from settings import base_context, templates

router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context=base_context,
    )
