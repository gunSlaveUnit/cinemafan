from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from movies.models import Movie
from settings import templates
from shared.utils import fill_base_context

router = APIRouter()


@router.get("/")
async def home(
        request: Request,
        base_context: dict = Depends(fill_base_context),
        db: AsyncSession = Depends(get_db),
):
    q = select(Movie).limit(5).order_by(Movie.created_at.desc())
    new = [await Movie.by_id(movie.id, db) async for movie in await db.stream_scalars(q)]

    extended_context = {"new": new}
    context = base_context
    context.update(extended_context)

    return templates.TemplateResponse(
        request=request,
        name="home/home.html",
        context=context,
    )
