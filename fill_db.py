import asyncio
from datetime import datetime
import random

from infrastructure.db import init, session_maker
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

FIXED_DATA = {
    "ages": [
        {
            "title": "G",
            "description": "all ages",
        },
        {
            "title": "PG",
            "description": "parental guidance",
        },
        {
            "title": "PG-13",
            "description": "parents strongly cautioned",
        },
        {
            "title": "R",
            "description": "restricted",
        },
        {
            "title": "NC-17",
            "description": "adults only",
        },
    ],
    "categories": [
        {"title": "full-length"},
        {"title": "series"},
        {"title": "short-length"},
    ],
    "genres": [
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
    ],
    "qualities": [
        {"resolution": 144},
        {"resolution": 240},
        {"resolution": 360},
        {"resolution": 480},
        {"resolution": 720},
        {"resolution": 1080},
        {"resolution": 2160},
        {"resolution": 4320},
    ],
}

ACTIVITIES_AMOUNT = 10
AGES_AMOUNT = len(FIXED_DATA["ages"])
CATEGORIES_AMOUNT = len(FIXED_DATA["categories"])
GENRES_AMOUNT = len(FIXED_DATA["genres"])
MAX_ACTIVITIES_PER_MOVIE_AMOUNT = 5
MAX_EPISODES_PER_SEASON_AMOUNT = 30
MAX_GENRES_PER_MOVIE_AMOUNT = 3
MAX_REVIEWS_PER_MOVIE_AMOUNT = 50
MAX_SCREENSHOTS_PER_MOVIE_AMOUNT = 10
MAX_SEASONS_PER_MOVIE_AMOUNT = 10
MAX_STUDIOS_PER_MOVIE_AMOUNT = 3
MAX_TAGS_PER_MOVIE_AMOUNT = 10
MOVIES_AMOUNT = 100
PERSONS_AMOUNT = 100
QUALITIES_AMOUNT = len(FIXED_DATA["qualities"])
STUDIOS_AMOUNT = 100
TAGS_AMOUNT = 100


async def fill():
    await init()

    async with session_maker() as db:
        try:
            for i in range(ACTIVITIES_AMOUNT):
                await Activity.create({"title": f"activity {i}"}, db)

            for age in FIXED_DATA["ages"]:
                await Age.create(age, db)

            for category in FIXED_DATA["categories"]:
                await Category.create(category, db)

            for genre in FIXED_DATA["genres"]:
                await Genre.create(genre, db)

            for i in range(PERSONS_AMOUNT):
                await Person.create({"name": f"person {i}"}, db)

            for quality in FIXED_DATA['qualities']:
                await Quality.create(quality, db)

            for i in range(STUDIOS_AMOUNT):
                await Studio.create({"title": f"studio {i}"}, db)

            for i in range(TAGS_AMOUNT):
                await Tag.create({"title": f"tag {i}"}, db)

            for i in range(MOVIES_AMOUNT):
                movie = {
                    "age_id": random.randint(1, AGES_AMOUNT),
                    "category_id": random.randint(1, CATEGORIES_AMOUNT),
                    "description": "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
                                   "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
                                   "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
                                   "consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum "
                                   "dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, "
                                   "sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "original_title": f"original language title {i}",
                    "poster": "poster.jpg",
                    "translated_title": f"any language title {i}",
                }
                await Movie.create(movie, db)

            created_seasons_amount = 0
            for i in range(MOVIES_AMOUNT):
                seasons_per_movie = random.randint(1, MAX_SEASONS_PER_MOVIE_AMOUNT)

                for j in range(seasons_per_movie):
                    season = {
                        "movie_id": i + 1,
                        "number": j,
                        "title": f"season {j}",
                    }
                    await Season.create(season, db)
                    created_seasons_amount += 1

            created_episodes_amount = 0
            for i in range(created_seasons_amount):
                episodes_per_season = random.randint(1, MAX_EPISODES_PER_SEASON_AMOUNT)

                for k in range(episodes_per_season):
                    episode = {
                        "number": k,
                        "parent_id": created_episodes_amount if created_episodes_amount > 0 else None,
                        "release_date": datetime.now(),
                        "season_id": i + 1,
                        "title": f"episode {k}",
                    }
                    await Episode.create(episode, db)
                    created_episodes_amount += 1

            for i in range(created_episodes_amount):
                for k in range(QUALITIES_AMOUNT):
                    record = {
                        "episode_id": i,
                        "filename": "video.mp4",
                        "quality_id": k + 1,
                    }
                    await Record.create(record, db)

            for i in range(MOVIES_AMOUNT):
                for _ in range(random.randint(1, MAX_GENRES_PER_MOVIE_AMOUNT)):
                    movie_genre = {
                        "genre_id": random.randint(1, GENRES_AMOUNT),
                        "movie_id": i + 1,
                    }
                    await MovieGenre.create(movie_genre, db)

            for i in range(MOVIES_AMOUNT):
                for _ in range(random.randint(1, MAX_ACTIVITIES_PER_MOVIE_AMOUNT)):
                    movie_person = {
                        "activity_id": random.randint(1, ACTIVITIES_AMOUNT),
                        "movie_id": i + 1,
                        "person_id": random.randint(1, PERSONS_AMOUNT),
                    }
                    await MoviePerson.create(movie_person, db)

            for i in range(MOVIES_AMOUNT):
                for _ in range(random.randint(1, MAX_STUDIOS_PER_MOVIE_AMOUNT)):
                    movie_studio = {
                        "movie_id": i + 1,
                        "studio_id": random.randint(1, STUDIOS_AMOUNT),
                    }
                    await MovieStudio.create(movie_studio, db)

            for i in range(MOVIES_AMOUNT):
                for _ in range(random.randint(1, MAX_TAGS_PER_MOVIE_AMOUNT)):
                    movie_tag = {
                        "movie_id": i + 1,
                        "relevance": random.randint(1, 1000),
                        "tag_id": random.randint(1, TAGS_AMOUNT),
                    }
                    await MovieTag.create(movie_tag, db)

            for i in range(MOVIES_AMOUNT):
                for j in range(random.randint(1, MAX_REVIEWS_PER_MOVIE_AMOUNT)):
                    review = {
                        "content": f"review {j}",
                        "movie_id": i + 1,
                    }
                    await Review.create(review, db)

            for i in range(MOVIES_AMOUNT):
                for j in range(random.randint(1, MAX_SCREENSHOTS_PER_MOVIE_AMOUNT)):
                    screenshot = {
                        "filename": "screenshot.jpg",
                        "movie_id": i + 1,
                        "title": f"screenshot {j}",
                    }
                    await Screenshot.create(screenshot, db)
        finally:
            await db.close()


asyncio.run(fill())
