import random

from fastapi import APIRouter, Request, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from infrastructure.settings import templates
from movies.models import Movie

router = APIRouter()


@router.get("/")
async def home(
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    count = await db.scalar(select(func.count()).select_from(Movie))
    result = await db.execute(select(Movie.id).offset(random.randint(1, count)))
    movie_id = result.scalars().first()

    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context={"movie_id": movie_id},
    )
