from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from infrastructure.settings import templates

from movies.models import (
    Activity,
    Age,
    Episode,
    Genre,
    Movie,
    MovieGenre,
    MoviePerson,
    MovieStudio,
    MovieTag,
    Person,
    Record,
    Quality,
    Season,
    Screenshot,
    Studio,
    Tag,
)

from infrastructure.db import get_db
from infrastructure.settings import templates

router = APIRouter(prefix="")


@router.get("/movies")
async def movies_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    data = [_ async for _ in Movie.every(db)]

    info = []
    for movie in data:
        seasons = [_ async for _ in Season.by_movie_id(movie.id, db)]
        seasons_count = len(seasons)

        age = await Age.by_id(movie.age_id, db)

        episodes = []
        for season in seasons:
            episodes.extend([_ async for _ in Episode.by_season_id(season.id, db)])
        episodes_count = len(episodes)

        movies_tags = [_ async for _ in MovieTag.by_movie_id(movie.id, db)]
        tags = []
        for movie_tag in movies_tags:
            tags.append(await Tag.by_id(movie_tag.tag_id, db))

        movie_genres = [_ async for _ in MovieGenre.by_movie_id(movie.id, db)]

        genres = []
        for movie_genre in movie_genres:
            genres.append(await Genre.by_id(movie_genre.genre_id, db))

        info.append({
            "movie": movie,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
            "tags": tags,
            "age": age,
            "genres": genres,
        })

    return templates.TemplateResponse(
        request=request,
        name="movies/index.html",
        context={
            "info": info,
        }
    )


@router.get("/movies/{item_id}")
async def movie_page(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(get_db)
):
    movie = await Movie.by_id(item_id, db)
    movie_id = movie.id

    seasons = [_ async for _ in Season.by_movie_id(movie_id, db)]
    seasons_count = len(seasons)

    episodes = []
    for season in seasons:
        episodes.extend([_ async for _ in Episode.by_season_id(season.id, db)])
    episodes_count = len(episodes)

    age = await Age.by_id(movie.age_id, db)

    screenshots = [_ async for _ in Screenshot.by_movie_id(movie_id, db)]

    movies_tags = [_ async for _ in MovieTag.by_movie_id(movie_id, db)]
    tags = []
    for movie_tag in movies_tags:
        tags.append(await Tag.by_id(movie_tag.tag_id, db))

    movie_studios = [_ async for _ in MovieStudio.by_movie_id(movie_id, db)]
    studios = []
    for movie_studio in movie_studios:
        studios.append(await Studio.by_id(movie_studio.studio_id, db))

    movie_genres = [_ async for _ in MovieGenre.by_movie_id(movie_id, db)]
    genres = []
    for movie_genre in movie_genres:
        genres.append(await Genre.by_id(movie_genre.genre_id, db))

    movie_persons = [_ async for _ in MoviePerson.by_movie_id(movie_id, db)]

    activities_persons = {}
    for movie_person in movie_persons:
        activity = await Activity.by_id(movie_person.activity_id, db)
        activities_persons[activity.title] = {
            "activity": activity,
            "persons": [],
        }

    for movie_person in movie_persons:
        activity = await Activity.by_id(movie_person.activity_id, db)
        activities_persons[activity.title]["persons"].append(await Person.by_id(movie_person.person_id, db))

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "age": age,
            "movie": movie,
            "episodes": episodes,
            "screenshots": screenshots,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
            "tags": tags,
            "genres": genres,
            "activities_persons": activities_persons,
            "studios": studios,
        }
    )


@router.get("/episodes/{item_id}")
async def episode_page(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(get_db)
):
    episode = await Episode.by_id(item_id, db)
    records = [_ async for _ in Record.by_episode_id(item_id, db)]
    qualities = [await Quality.by_id(record.quality_id, db) for record in records]

    return templates.TemplateResponse(
        request=request,
        name="movies/episode.html",
        context={
            "episode": episode,
            "records": records,
            "qualities": qualities
        }
    )