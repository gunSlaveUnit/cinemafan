import random

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from infrastructure.settings import templates
from movies.models import Movie

router = APIRouter(prefix="")


@router.get("/")
async def home(
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    data = [_ async for _ in Movie.every(db)]

    context = {}
    movie_id = None
    if data:
        movie_id = random.choice(data).id
    context["movie_id"] = movie_id

    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context=context,
    )
