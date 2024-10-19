import asyncio
from datetime import datetime
import random
import subprocess
import uuid

from db import init, session_maker
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
    Tag,
)
from settings import MEDIA_DIR

ACTIVITIES_AMOUNT = 10
PERSONS_AMOUNT = 2000
STUDIOS_AMOUNT = 100
MAX_EPISODES_PER_SEASON_AMOUNT = 50
MAX_GENRES_PER_MOVIE_AMOUNT = 5
MAX_REVIEWS_PER_MOVIE_AMOUNT = 1000
MAX_SCREENSHOTS_PER_MOVIE_AMOUNT = 10
MAX_SEASONS_PER_MOVIE_AMOUNT = 10
MAX_STUDIOS_PER_MOVIE_AMOUNT = 3
MAX_PERSONS_PER_MOVIE_AMOUNT = 20
MAX_TAGS_PER_MOVIE_AMOUNT = 30
MOVIES_AMOUNT = 10000
TAGS_AMOUNT = 1000

ACTIVITIES = [{"title": f"activity {i}"} for i in range(ACTIVITIES_AMOUNT)]
AGES = [
    {"title": "G", "description": "all ages"},
    {"title": "PG", "description": "parental guidance"},
    {"title": "PG-13", "description": "parents strongly cautioned"},
    {"title": "R", "description": "restricted"},
    {"title": "NC-17", "description": "adults only"},
]
CATEGORIES = [
    {"title": "full-length"},
    {"title": "series"},
    {"title": "short-length"},
]
GENRES = [
    {"title": "action"},
    {"title": "adventure"},
    {"title": "animated"},
    {"title": "comedy"},
    {"title": "drama"},
    {"title": "fantasy"},
    {"title": "historical"},
    {"title": "horror"},
    {"title": "musical"},
    {"title": "noir"},
    {"title": "romance"},
    {"title": "science fiction"},
    {"title": "thriller"},
    {"title": "western"},
]
PERSONS = [{"name": f"person {i}"} for i in range(PERSONS_AMOUNT)]
QUALITIES = [
    {"resolution": 144},
    {"resolution": 240},
    {"resolution": 360},
    {"resolution": 480},
    {"resolution": 720},
    {"resolution": 1080},
    {"resolution": 2160},
    {"resolution": 4320},
    {"resolution": 8640},
]
STUDIOS = [{"title": f"studio {i}"} for i in range(STUDIOS_AMOUNT)]
TAGS = [{"title": f"tag {i}"} for i in range(TAGS_AMOUNT)]
MOVIES = [
    {
        "age_id": AGES[random.randint(0, len(AGES) - 1)]["id"],
        "category_id": CATEGORIES[random.randint(0, len(CATEGORIES) - 1)]["id"],
        "description": "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
                        "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
                        "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
                        "consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum "
                        "dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, "
                        "sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "original_title": f"original language title {i}",
        "poster": "poster.jpg",
        "translated_title": f"any language title {i}",
    } for i in range(MOVIES_AMOUNT)
]
MOVIE_SEASONS = []
for movie in MOVIES:
    seasons = []
    for i in range(random.randint(1, MAX_SEASONS_PER_MOVIE_AMOUNT)):
        seasons.append({
            "movie_id": movie["id"],
            "number": i + 1,
            "title": f"season {i}",
        })
    MOVIE_SEASONS.append(seasons)
EPISODES = []
for seasons in MOVIE_SEASONS:
    parent_id = None
    for season in seasons:
        for i in range(random.randint(1, MAX_EPISODES_PER_SEASON_AMOUNT)):
            episode = {
                "duration": float(subprocess.check_output([
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    MEDIA_DIR / "video.mp4",
                ]).decode("utf-8")),
                "number": i,
                "parent_id": parent_id,
                "release_date": datetime.now(),
                "season_id": season["id"],
                "title": f"episode {i}",
            }
            EPISODES.append(episode)
            parent_id = episode["id"]
EPISODE_RECORDS = [
    [
        {
            "episode_id": episode["id"],
            "filename": "video.mp4",
            "quality_id": quality["id"],
        } for quality in QUALITIES
    ] for episode in EPISODES
]
MOVIE_GENRES = [
    [
        {
            "movie_id": movie["id"],
            "genre_id": random.choice(GENRES)["id"],
        } for _ in range(random.randint(1, MAX_GENRES_PER_MOVIE_AMOUNT))
    ] for movie in MOVIES
]
MOVIE_PERSONS = [
    [
        {
            "activity_id": random.choice(ACTIVITIES)["id"],
            "movie_id": movie["id"],
            "person_id": random.choice(PERSONS)["id"],
        } for _ in range(random.randint(1, MAX_PERSONS_PER_MOVIE_AMOUNT))
    ] for movie in MOVIES
]
MOVIE_STUDIOS = [
    [
        {
            "movie_id": movie["id"],
            "studio_id": random.choice(STUDIOS)["id"],
        } for _ in range(random.randint(1, MAX_STUDIOS_PER_MOVIE_AMOUNT))
    ] for movie in MOVIES
]
MOVIE_TAGS = [
    [
        {
            "movie_id": movie["id"],
            "relevance": random.randint(1, 1000),
            "tag_id": random.choice(TAGS)["id"],
        } for _ in range(random.randint(1, MAX_TAGS_PER_MOVIE_AMOUNT))
    ] for movie in MOVIES
]
MOVIE_REVIEWS = [
    [
        {
            "movie_id": movie["id"],
            "content": f"review {i}",
        } for i in range(random.randint(1, MAX_REVIEWS_PER_MOVIE_AMOUNT))
    ] for movie in MOVIES
]
MOVIE_SCREENSHOTS = [
    [
        {
            "movie_id": movie["id"],
            "title": f"screenshot {i}",
            "filename": "screenshot.jpg",
        } for i in range(random.randint(1, MAX_SCREENSHOTS_PER_MOVIE_AMOUNT))
    ] for movie in MOVIES
]

async def fill():
    await init()

    async with session_maker() as db:
        try:
            for activity in ACTIVITIES:
                await Activity.create(activity, db)

            for age in AGES:
                await Age.create(age, db)

            for category in CATEGORIES:
                await Category.create(category, db)

            for genre in GENRES:
                await Genre.create(genre, db)

            for person in PERSONS:
                await Person.create(person, db)

            for quality in QUALITIES:
                await Quality.create(quality, db)

            for studio in STUDIOS:
                await Studio.create(studio, db)

            for tag in TAGS:
                await Tag.create(tag, db)

            for movie in MOVIES:
                await Movie.create(movie, db)

            for seasons in MOVIE_SEASONS:
                for season in seasons:
                    await Season.create(season, db)

            for episode in EPISODES:
                await Episode.create(episode, db)

            for records in EPISODE_RECORDS:
                for record in records:
                    await Record.create(record, db)

            for genres in MOVIE_GENRES:
                for genre in genres:
                    await MovieGenre.create(genre, db)

            for persons in MOVIE_PERSONS:
                for person in persons:
                    await MoviePerson.create(person, db)

            for studios in MOVIE_STUDIOS:
                for studio in studios:
                    await MovieStudio.create(studio, db)

            for tags in MOVIE_TAGS:
                for tag in tags:
                    await MovieTag.create(tag, db)

            for reviews in MOVIE_REVIEWS:
                for review in reviews:
                    await Review.create(review, db)

            for screenshots in MOVIE_SCREENSHOTS:
                for screenshot in screenshots:
                    await Screenshot.create(screenshot, db)
        finally:
            await db.close()


asyncio.run(fill())
