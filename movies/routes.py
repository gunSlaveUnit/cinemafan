import random
import subprocess
import typing
import uuid
import math

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from db import get_db
from movies.models import (
    Activity,
    Age,
    Category,
    Country,
    Episode,
    Genre,
    Moment,
    Movie,
    MovieCountry,
    MovieGenre,
    MoviePerson,
    MoviePlaylist,
    MovieStudio,
    MovieTag,
    Person,
    Playlist,
    Rating,
    Record,
    Review,
    Quality,
    Season,
    Screenshot,
    Status,
    Studio,
    Tag,
    Upvote,
)
from movies.schemas import ReviewCreateSchema, MomentCreateSchema
from settings import MEDIA_DIR, templates
from shared.utils import fill_base_context, get_current_user

router = APIRouter(prefix="")


def format_years(years):
    years = sorted(set(years))
    
    periods = []
    period_start = years[0]
    previous = years[0]
    
    for year in years[1:] + [None]:
        if year != previous + 1:
            if period_start != previous:
                periods.append(f"{period_start} - {previous}")
            else:
                periods.append(str(period_start))
            period_start = year
        previous = year
    
    return ", ".join(periods)


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
        q = select(func.avg(Rating.value)).select_from(Rating).where(Rating.movie_id == movie.id)
        rating = await db.scalar(q)

        q = select(func.count()).select_from(Rating).where(Rating.movie_id == movie.id)
        ratings_amount = await db.scalar(q)

        age = await Age.by_id(movie.age_id, db)

        q = select(MovieCountry).where(MovieCountry.movie_id == movie.id).limit(3)
        movie_countries = await db.stream_scalars(q)
        countries = [await Country.by_id(movie_country.country_id, db) async for movie_country in movie_countries]

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

        years = []
        q = select(Season).where(Season.movie_id == movie.id)
        seasons = await db.stream_scalars(q)
        async for season in seasons:
            q = select(Episode).where(Episode.season_id == season.id)
            episodes = await db.stream_scalars(q)
            async for episode in episodes:
                years.append(episode.release_date.year)
        
        q = select(MovieGenre).where(MovieGenre.movie_id == movie.id).limit(5)
        movie_genres = await db.stream_scalars(q)
        genres = [await Genre.by_id(movie_genre.genre_id, db) async for movie_genre in movie_genres]

        q = (
            select(
                MovieTag.tag_id,
                func.count(Upvote.movie_tag_id)
            )
            .join(
                Upvote,
                Upvote.movie_tag_id == MovieTag.id
            )
            .where(MovieTag.movie_id == movie.id)
            .group_by(MovieTag.tag_id)
            .order_by(
                func.count(Upvote.movie_tag_id).desc()
            )
            .limit(5)
        )
        result = await db.stream(q)
        tags = []
        async for row in result:
            tag_id = row[0]
            tag = await Tag.by_id(tag_id, db)
            tags.append(tag)

        status = await Status.by_id(movie.status_id, db)

        items.append({
            "age": age,
            "duration": f"{duration:.2f}h",
            "episodes_amount": episodes_amount,
            "episode_duration": f"{episode_duration:.2f}m",
            "countries": countries,
            "genres": genres,
            "movie": movie,
            "status": status,
            "seasons_amount": seasons_amount,
            "tags": tags,
            "years": format_years(years),
            "rating": rating,
            "ratings_amount": ratings_amount,
        })

    q = select(func.count()).select_from(Movie)
    count = await db.scalar(q)

    pages = math.ceil(count / limit)

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "count": count,
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
        return RedirectResponse("/")


@router.get("/movies/{item_id}")
async def movie(
        request: Request,
        item_id: uuid.UUID,
        base_context: dict = Depends(fill_base_context),
        db: AsyncSession = Depends(get_db),
):
    item = await Movie.by_id(item_id, db)

    q = select(func.avg(Rating.value)).select_from(Rating).where(Rating.movie_id == item_id)
    rating = await db.scalar(q)

    q = select(func.count()).select_from(Rating).where(Rating.movie_id == item_id)
    ratings_amount = await db.scalar(q)

    years = []
    q = select(Season).where(Season.movie_id == item_id)
    seasons = await db.stream_scalars(q)
    async for season in seasons:
        q = select(Episode).where(Episode.season_id == season.id)
        episodes = await db.stream_scalars(q)
        async for episode in episodes:
            years.append(episode.release_date.year)

    age = await Age.by_id(item.age_id, db)

    q = select(func.count()).select_from(Season).where(Season.movie_id == item.id)
    seasons_amount = await db.scalar(q)

    episodes_amount = 0
    q = select(Season).where(Season.movie_id == item.id)
    seasons = await db.stream_scalars(q)
    async for season in seasons:
        q = select(func.count()).select_from(Episode).where(Episode.season_id == season.id)
        episodes_amount += await db.scalar(q)

    duration = 0.0
    q = select(Season).where(Season.movie_id == item.id)
    seasons = await db.stream_scalars(q)
    async for season in seasons:
        q = select(func.sum(Episode.duration)).select_from(Episode).where(Episode.season_id == season.id)
        duration += await db.scalar(q)

    episode_duration = duration / episodes_amount

    duration /= 3600
    episode_duration /= 60

    seasons = [{"season": _, "episodes": []} async for _ in Season.by_movie_id(item.id, db)]
    for season in seasons:
        season["episodes"] = [_ async for _ in Episode.by_season_id(season["season"].id, db)]

    q = select(MovieGenre).where(MovieGenre.movie_id == item.id).limit(5)
    movie_genres = await db.stream_scalars(q)
    genres = [await Genre.by_id(movie_genre.genre_id, db) async for movie_genre in movie_genres]

    q = (
        select(
            MovieTag,
            func.count(Upvote.movie_tag_id).label('relevance')
        )
        .outerjoin(
            Upvote,
            Upvote.movie_tag_id == MovieTag.id
        )
        .where(MovieTag.movie_id == item.id)
        .group_by(MovieTag)
        .order_by(func.count(Upvote.movie_tag_id).desc())
        .limit(5)
    )

    result = await db.execute(q)
    tags = [
        {
            "movie_tag": movie_tag,
            "tag": await Tag.by_id(movie_tag.tag_id, db),
            "relevance": relevance or 0
        }
        for movie_tag, relevance in result.all()
    ]

    status = await Status.by_id(item.status_id, db)

    # TODO: possible lots items
    screenshots = [_ async for _ in Screenshot.by_movie_id(item.id, db)]

    # TODO: possible lots items
    q = select(MovieStudio).where(MovieStudio.movie_id == item.id).limit(3)
    movie_studios = await db.stream_scalars(q)
    studios = [await Studio.by_id(movie_studio.studio_id, db) async for movie_studio in movie_studios]

    movie_persons = [_ async for _ in MoviePerson.by_movie_id(item.id, db)]

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

    # TODO: possible lots items
    reviews = [_ async for _ in Review.by_movie_id(item.id, db)]

    extended_context = {
        "age": age,
        "duration": f"{duration:.2f}h",
        "episodes_amount": episodes_amount,
        "episode_duration": f"{episode_duration:.2f}m",
        "movie": item,
        "screenshots": screenshots,
        "tags": tags,
        "genres": genres,
        "activities_persons": activities_persons,
        "seasons_amount": seasons_amount,
        "seasons": seasons,
        "status": status,
        "studios": studios,
        "reviews": reviews,
        "years": format_years(years),
        "rating": rating,
        "ratings_amount": ratings_amount,
    }
    context = base_context
    context.update(extended_context)

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context=context,
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

    q = select(Episode).where(Episode.parent_id == item_id)
    next_episode = await db.scalar(q)

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
            "next_episode": next_episode,
        }
    )


@router.patch("/api/movies-tags/{item_id}/bump")
async def bump_tag(
        item_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    upvote = await db.scalar(select(Upvote).where(Upvote.movie_tag_id == item_id, Upvote.user_id == current_user.id))
    if upvote:
        raise HTTPException(status_code=409, detail="You already upvoted this tag")

    await Upvote.create(
        {
            "movie_tag_id": item_id,
            "user_id": current_user.id
        },
        db
    )


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
