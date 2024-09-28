import json
import subprocess

from fastapi import APIRouter, Request, Depends
from ffmpeg.asyncio import FFmpeg
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.settings import MEDIA_DIR

from infrastructure.db import get_db
from infrastructure.settings import templates

from movies.models import (
    Activity,
    Age,
    Category,
    Episode,
    Genre,
    Movie,
    MovieGenre,
    MoviePerson,
    MovieStudio,
    MovieTag,
    Person,
    Record,
    Review,
    Quality,
    Season,
    Screenshot,
    Studio,
    Tag, Moment,
)
from movies.schemas import ReviewCreateSchema, MomentCreateSchema

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

        duration = 0.0
        for episode in episodes:
            records = [_ async for _ in Record.by_episode_id(episode.id, db)]
            episode_duration = subprocess.check_output([
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                MEDIA_DIR / records[0].filename,
            ])
            duration += float(episode_duration.decode("utf-8"))

        info.append({
            "movie": movie,
            "episodes_count": episodes_count,
            "seasons_count": seasons_count,
            "tags": tags,
            "age": age,
            "genres": genres,
            "duration": duration,
        })

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
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
        item_id: int,
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
        item_id: int,
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
        item_id: int,
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
        item_id: int,
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
        item_id: int,
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
