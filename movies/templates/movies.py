from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.api import movies
from movies.models import Episode, Age, Season, Screenshot, Tagging, Tag
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
        seasons = [_ async for _ in Season.by_movie_id(movie.id, db)]
        seasons_count = len(seasons)

        episodes = []
        for season in seasons:
            episodes.extend([_ async for _ in Episode.by_season_id(season.id, db)])
        episodes_count = len(episodes)

        taggings = [_ async for _ in Tagging.by_movie_id(movie.id, db)]
        tags = []
        for tagging in taggings:
            tags.append(await Tag.by_id(tagging.tag_id, db))

        info.append({
            "movie": movie,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
            "tags": tags,
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

    seasons = [_ async for _ in Season.by_movie_id(movie_id, db)]
    seasons_count = len(seasons)

    episodes = []
    for season in seasons:
        episodes.extend([_ async for _ in Episode.by_season_id(season.id, db)])
    episodes_count = len(episodes)

    age = await Age.by_id(response.age_id, db)

    screenshots = [_ async for _ in Screenshot.by_movie_id(movie_id, db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "age": age,
            "movie": response,
            "episodes": episodes,
            "screenshots": screenshots,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
        }
    )
