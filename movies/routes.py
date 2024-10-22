import json
import random
import subprocess
import typing
import uuid
import math

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import RedirectResponse
from ffmpeg.asyncio import FFmpeg
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from settings import MEDIA_DIR

from db import get_db
from settings import templates

from movies.models import (
    Activity,
    Age,
    Category,
    Episode,
    Genre,
    Moment,
    Movie,
    MovieGenre,
    MoviePerson,
    MoviePlaylist,
    MovieStudio,
    MovieTag,
    Person,
    Playlist,
    Record,
    Review,
    Quality,
    Season,
    Screenshot,
    Studio,
    Tag,
)
from movies.schemas import ReviewCreateSchema, MomentCreateSchema

from db import get_db
from settings import templates

router = APIRouter(prefix="")


@router.get("/movies")
async def movies(
        request: Request,
        page: typing.Annotated[int, Query(ge=0)] = 0,
        limit: typing.Annotated[int, Query(ge=1, le=50)] = 10,
        db: AsyncSession = Depends(get_db),
) -> templates.TemplateResponse:
    items = []

    q = select(Movie).limit(limit).offset(page * limit)
    data = await db.stream_scalars(q)
    
    async for movie in data:
        age = await Age.by_id(movie.age_id, db)

        q = select(func.count()).select_from(Season).where(Season.movie_id == movie.id)
        seasons_amount = await db.scalar(q)

        episodes_amount = 0
        q = select(Season).where(Season.movie_id == movie.id)
        seasons = await db.stream_scalars(q)
        async for season in seasons:
            q = select(func.count()).select_from(Episode).where(Episode.season_id == season.id)
            episodes_amount += await db.scalar(q)

        duration = 0.0
        q = select(Season).where(Season.movie_id == movie.id)
        seasons = await db.stream_scalars(q)
        async for season in seasons:
            q = select(func.sum(Episode.duration)).select_from(Episode).where(Episode.season_id == season.id)
            duration += await db.scalar(q)

        episode_duration = duration / episodes_amount

        duration /= 3600
        episode_duration /= 60

        q = select(MovieGenre).where(MovieGenre.movie_id == movie.id).limit(5)
        movie_genres = await db.stream_scalars(q)
        genres = [await Genre.by_id(movie_genre.genre_id, db) async for movie_genre in movie_genres]

        q = select(MovieTag).where(MovieTag.movie_id == movie.id).order_by(MovieTag.relevance.desc()).limit(5)
        movie_tags = await db.stream_scalars(q)
        tags = [await Tag.by_id(movie_tag.tag_id, db) async for movie_tag in movie_tags]

        items.append({
            "age": age,
            "duration": f"{duration:.2f}h",
            "episodes_amount": episodes_amount,
            "episode_duration": f"{episode_duration:.2f}m",
            "genres": genres,
            "movie": movie,
            "seasons_amount": seasons_amount,
            "tags": tags,
        })

    q = select(func.count()).select_from(Movie)
    count = await db.scalar(q)

    pages = math.ceil(count / limit)

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "items": items,
            "pages": pages,
        }
    )


@router.get("/playlists")
async def playlists(
        request: Request,
        page: typing.Annotated[int, Query(ge=0)] = 0,
        limit: typing.Annotated[int, Query(ge=1, le=50)] = 10,
        db: AsyncSession = Depends(get_db),
) -> templates.TemplateResponse:
    q = select(Playlist).limit(limit).offset(page * limit)
    data = await db.stream_scalars(q)
    items = [_ async for _ in data]

    q = select(func.count()).select_from(Playlist)
    count = await db.scalar(q)

    pages = math.ceil(count / limit)

    return templates.TemplateResponse(
        request=request,
        name="movies/playlists.html",
        context={
            "items": items,
            "pages": pages,
        }
    )


@router.get("/playlists/{item_id}")
async def playlist(
        request: Request,
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    item = await Playlist.by_id(item_id, db)

    
    q = select(MoviePlaylist).where(MoviePlaylist.playlist_id == item_id)
    movies = [await Movie.by_id(movie_playlist.movie_id, db) async for movie_playlist in await db.stream_scalars(q)]

    return templates.TemplateResponse(
        request=request,
        name="movies/playlist.html",
        context={
            "playlist": item,
            "movies": movies,
        }
    )


@router.get("/movies/random")
async def random_movie_page(
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    count = await db.scalar(select(func.count()).select_from(Movie))

    if count == 0:
        movie_id = None
    else:
        result = await db.execute(select(Movie.id).offset(random.randint(0, count - 1)))
        movie_id = result.scalars().first()

    if movie_id:
        return RedirectResponse(f"/movies/{movie_id}")
    else:
        return RedirectResponse(f"/")


@router.get("/movies/{item_id}")
async def movie_page(
        request: Request,
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    movie = await Movie.by_id(item_id, db)
    movie_id = movie.id

    seasons = [{"season": _, "episodes": []} async for _ in Season.by_movie_id(movie_id, db)]
    for season in seasons:
        season["episodes"] = [_ async for _ in Episode.by_season_id(season["season"].id, db)]
    seasons_count = len(seasons)

    episodes_count = 0
    for season in seasons:
        episodes_count += len(season["episodes"])

    age = await Age.by_id(movie.age_id, db)

    screenshots = [_ async for _ in Screenshot.by_movie_id(movie_id, db)]

    movies_tags = [{"movie_tag": _, "tag": None} async for _ in MovieTag.by_movie_id(movie_id, db)]
    for movie_tag in movies_tags:
        movie_tag["tag"] = await Tag.by_id(movie_tag["movie_tag"].tag_id, db)

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

    reviews = [_ async for _ in Review.by_movie_id(movie_id, db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "age": age,
            "movie": movie,
            "screenshots": screenshots,
            "seasons": seasons,
            "seasons_count": seasons_count,
            "episodes_count": episodes_count,
            "tags": movies_tags,
            "genres": genres,
            "activities_persons": activities_persons,
            "studios": studios,
            "reviews": reviews,
        }
    )


@router.get("/episodes/{item_id}")
async def episode_page(
        request: Request,
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    episode = await Episode.by_id(item_id, db)
    moments = [_ async for _ in Moment.by_episode_id(item_id, db)]
    records = [_ async for _ in Record.by_episode_id(item_id, db)]
    qualities = [await Quality.by_id(record.quality_id, db) for record in records]

    duration = subprocess.check_output([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        MEDIA_DIR / records[0].filename,
    ])
    duration = float(duration.decode("utf-8"))

    return templates.TemplateResponse(
        request=request,
        name="movies/episode.html",
        context={
            "duration": duration,
            "episode": episode,
            "moments": moments,
            "records": records,
            "qualities": qualities,
        }
    )


@router.patch("/api/movies-tags/{item_id}/bump")
async def bump_tag(
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    movie_tag = await MovieTag.by_id(item_id, db)
    await movie_tag.update({"relevance": movie_tag.relevance + 1}, db)


@router.post("/api/reviews")
async def create(
        data: ReviewCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await Review.create(data.model_dump(), db)


@router.get("/studios/{item_id}")
async def studio_page(
        request: Request,
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    studio = await Studio.by_id(item_id, db)
    movies_studios = [_ async for _ in MovieStudio.by_studio_id(studio.id, db)]
    data = [await Movie.by_id(movie_studio.movie_id, db) for movie_studio in movies_studios]

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
        name="movies/studio.html",
        context={
            "info": info,
            "studio": studio,
        }
    )


@router.post("/api/moments")
async def create_moment(
        data: MomentCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await Moment.create(data.model_dump(), db)



@router.get("/activities/{item_id}")
async def activity_page(
        request: Request,
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    activity = await Activity.by_id(item_id, db)
    movies_persons = [_ async for _ in MoviePerson.by_activity_id(activity.id, db)]
    persons = [await Person.by_id(movie_person.person_id, db) for movie_person in movies_persons]

    return templates.TemplateResponse(
        request=request,
        name="movies/activity.html",
        context={
            "activity": activity,
            "persons": persons,
        },
    )



@router.get("/persons/{item_id}")
async def person_page(
        request: Request,
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    person = await Person.by_id(item_id, db)
    movies_persons = [_ async for _ in MoviePerson.by_person_id(person.id, db)]
    data = [await Movie.by_id(movie_person.movie_id, db) for movie_person in movies_persons]

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
        name="movies/person.html",
        context={
            "info": info,
            "person": person,
        }
    )


@router.get("/activities")
async def activities_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    data = [_ async for _ in Activity.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/activities.html",
        context={"activities": data},
    )


@router.get("/ages")
async def ages_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    data = [_ async for _ in Age.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/ages.html",
        context={"ages": data},
    )


@router.get("/categories")
async def categories_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    data = [_ async for _ in Category.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/categories.html",
        context={"categories": data},
    )


@router.get("/genres")
async def genres_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    data = [_ async for _ in Genre.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/genres.html",
        context={"genres": data},
    )


@router.get("/studios")
async def studios_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    data = [_ async for _ in Studio.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/studios.html",
        context={"studios": data},
    )


@router.get("/persons")
async def persons_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    persons = [_ async for _ in Person.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/persons.html",
        context={"persons": persons},
    )


@router.get("/tags")
async def tags_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    tags = [_ async for _ in Tag.every(db)]

    return templates.TemplateResponse(
        request=request,
        name="movies/tags.html",
        context={"tags": tags},
    )
