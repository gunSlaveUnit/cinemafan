import random

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from infrastructure.settings import templates
from movies.api import movies

router = APIRouter(prefix="", tags=["root"])


@router.get("/")
async def index(
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    response = await movies.items(db)
    data = response["data"]

    context = {}
    movie_id = None
    if data:
        movie_id = random.choice(data).id
    context["movie_id"] = movie_id

    return templates.TemplateResponse(
        request=request,
        name="root/index.html",
        context=context,
    )
