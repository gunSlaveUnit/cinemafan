from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.api import movies
from movies.models import Episode, Age
from infrastructure.db import session
from infrastructure.settings import templates

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("")
async def items(
        request: Request,
        db: AsyncSession = Depends(session)
):
    response = await movies.items(db)
    data = response["data"]

    info = []
    for movie in data:
        episodes = [_ async for _ in Episode.by_movie_id(movie.id, db)]
        episodes_count = len(episodes)
        seasons_count = len(set(episode.season for episode in episodes))
        info.append({
            "movie": movie,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
        })

    return templates.TemplateResponse(
        request=request,
        name="movies/index.html",
        context={
            "info": info,
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
    episodes_count = len(episodes)
    seasons_count = len(set(episode.season for episode in episodes))
    age = await Age.by_id(response.age_id, db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "age": age,
            "movie": response,
            "episodes": episodes,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
        }
    )
