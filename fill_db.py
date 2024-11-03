import asyncio
import datetime
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
)
from settings import MEDIA_DIR

ACTIVITIES_AMOUNT = 10
PERSONS_AMOUNT = 50
PLAYLISTS_AMOUNT = 10
STUDIOS_AMOUNT = 50
MAX_EPISODES_PER_SEASON_AMOUNT = 12
MAX_GENRES_PER_MOVIE_AMOUNT = 5
MAX_RATINGS_PER_MOVIE_AMOUNT = 50
MAX_REVIEWS_PER_MOVIE_AMOUNT = 30
MAX_SCREENSHOTS_PER_MOVIE_AMOUNT = 10
MAX_SEASONS_PER_MOVIE_AMOUNT = 5
MAX_STUDIOS_PER_MOVIE_AMOUNT = 3
MAX_PERSONS_PER_MOVIE_AMOUNT = 30
MAX_PLAYLISTS_PER_MOVIE_AMOUNT = 5
MAX_TAGS_PER_MOVIE_AMOUNT = 15
MOVIES_AMOUNT = 10
TAGS_AMOUNT = 100

ACTIVITIES = [{"id": uuid.uuid4(), "title": f"activity {i}"} for i in range(ACTIVITIES_AMOUNT)]
AGES = [
    {"id": uuid.uuid4(), "title": "G", "description": "all ages"},
    {"id": uuid.uuid4(), "title": "PG", "description": "parental guidance"},
    {"id": uuid.uuid4(), "title": "PG-13", "description": "parents strongly cautioned"},
    {"id": uuid.uuid4(), "title": "R", "description": "restricted"},
    {"id": uuid.uuid4(), "title": "NC-17", "description": "adults only"},
]
CATEGORIES = [
    {"id": uuid.uuid4(), "title": "full-length"},
    {"id": uuid.uuid4(), "title": "series"},
    {"id": uuid.uuid4(), "title": "short-length"},
]
GENRES = [
    {"id": uuid.uuid4(), "title": "action"},
    {"id": uuid.uuid4(), "title": "adventure"},
    {"id": uuid.uuid4(), "title": "animated"},
    {"id": uuid.uuid4(), "title": "comedy"},
    {"id": uuid.uuid4(), "title": "drama"},
    {"id": uuid.uuid4(), "title": "fantasy"},
    {"id": uuid.uuid4(), "title": "historical"},
    {"id": uuid.uuid4(), "title": "horror"},
    {"id": uuid.uuid4(), "title": "musical"},
    {"id": uuid.uuid4(), "title": "noir"},
    {"id": uuid.uuid4(), "title": "romance"},
    {"id": uuid.uuid4(), "title": "science fiction"},
    {"id": uuid.uuid4(), "title": "thriller"},
    {"id": uuid.uuid4(), "title": "western"},
]
PERSONS = [{"id": uuid.uuid4(), "name": f"person {i}"} for i in range(PERSONS_AMOUNT)]
PLAYLISTS = [
    {"id": uuid.uuid4(), "title": f"playlist {i}"} for i in range(PLAYLISTS_AMOUNT)
]
QUALITIES = [
    {"id": uuid.uuid4(), "resolution": 144},
    {"id": uuid.uuid4(), "resolution": 240},
    {"id": uuid.uuid4(), "resolution": 360},
    {"id": uuid.uuid4(), "resolution": 480},
    {"id": uuid.uuid4(), "resolution": 720},
    {"id": uuid.uuid4(), "resolution": 1080},
    {"id": uuid.uuid4(), "resolution": 2160},
    {"id": uuid.uuid4(), "resolution": 4320},
    {"id": uuid.uuid4(), "resolution": 8640},
]
STATUSES = [
    {"id": uuid.uuid4(), "title": "completed"},
    {"id": uuid.uuid4(), "title": "ongoing"},
]
STUDIOS = [{"id": uuid.uuid4(), "title": f"studio {i}"} for i in range(STUDIOS_AMOUNT)]
TAGS = [{"id": uuid.uuid4(), "title": f"tag {i}"} for i in range(TAGS_AMOUNT)]
MOVIES = [
    {
        "id": uuid.uuid4(), 
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
        "status_id": STATUSES[random.randint(0, len(STATUSES) - 1)]["id"],
        "translated_title": f"any language title {i}",
    } for i in range(MOVIES_AMOUNT)
]
MOVIE_SEASONS = []
for movie in MOVIES:
    seasons = []
    for i in range(random.randint(1, MAX_SEASONS_PER_MOVIE_AMOUNT)):
        seasons.append({
            "id": uuid.uuid4(),
            "movie_id": movie["id"],
            "number": i + 1,
            "title": f"season {i}",
        })
    MOVIE_SEASONS.append(seasons)

RATINGS = []
for movie in MOVIES:
    for i in range(random.randint(0, MAX_RATINGS_PER_MOVIE_AMOUNT)):
        RATINGS.append({
            "movie_id": movie["id"],
            "value": random.randint(1, 10),
        })

EPISODES = []
for seasons in MOVIE_SEASONS:
    parent_id = None
    for season in seasons:
        for i in range(random.randint(1, MAX_EPISODES_PER_SEASON_AMOUNT)):
            episode = {
                "id": uuid.uuid4(),
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
                "release_date": datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365 * 50)),
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
MOVIE_PLAYLISTS = [
    [
        {
            "movie_id": movie["id"],
            "playlist_id": random.choice(PLAYLISTS)["id"],
        } for _ in range(random.randint(1, MAX_PLAYLISTS_PER_MOVIE_AMOUNT))
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

            for playlist in PLAYLISTS:
                await Playlist.create(playlist, db)

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

            for rating in RATINGS:
                await Rating.create(rating, db)

            for records in EPISODE_RECORDS:
                for record in records:
                    await Record.create(record, db)

            for genres in MOVIE_GENRES:
                for genre in genres:
                    await MovieGenre.create(genre, db)

            for persons in MOVIE_PERSONS:
                for person in persons:
                    await MoviePerson.create(person, db)

            for playlists in MOVIE_PLAYLISTS:
                for playlist in playlists:
                    await MoviePlaylist.create(playlist, db)

            for statuses in STATUSES:
                await Status.create(statuses, db)

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
