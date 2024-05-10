from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.api import movies
from movies.models import Episode
from root.db import session
from root.settings import templates

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def items(
        request: Request,
        db: AsyncSession = Depends(session)
):
    response = await movies.items(db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "movies": response["data"],
        }
    )


@router.get("/{item_id}")
async def item(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(session)
):
    response = await movies.item(item_id, db)
    movie_id = response.id
    episodes = [_ async for _ in Episode.by_movie_id(movie_id, db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "movie": response,
            "episodes": episodes,
        }
    )
