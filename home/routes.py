from fastapi import APIRouter, Depends, Request

from settings import templates
from shared.utils import fill_base_context

router = APIRouter()


@router.get("/")
async def home(
        request: Request,
        base_context: dict = Depends(fill_base_context),
):
    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context=base_context,
    )
