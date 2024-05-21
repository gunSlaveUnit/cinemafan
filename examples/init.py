import asyncio
import json
import datetime

from movies.models import Age, Movie, Episode, Quality, Record, Category, Season, Screenshot, Tag, Tagging, Genre, \
    MovieGenre, Person, Activity, MoviePerson
from infrastructure.db import session_maker
from movies.schemas import AgeCreateSchema, MovieCreateSchema, EpisodeCreateSchema, QualityCreateSchema, \
    RecordCreateSchema, CategoryCreateSchema, SeasonCreateSchema, ScreenshotCreateSchema, TagCreateSchema, \
    TaggingCreateSchema, GenreCreateSchema, MovieGenreCreateSchema, MoviePersonCreateSchema, PersonCreateSchema, \
    ActivityCreateSchema


async def create_ages_from_json(data):
    async with session_maker() as s:
        try:
            for age_data in data['ages']:
                await Age.create(
                    AgeCreateSchema(title=age_data['title'], description=age_data['description']).model_dump(), s)
        finally:
            await s.close()


async def create_categories_from_json(data):
    async with session_maker() as s:
        try:
            for category_data in data['categories']:
                await Category.create(CategoryCreateSchema(title=category_data['title']).model_dump(), s)
        finally:
            await s.close()


async def create_qualities_from_json(data):
    async with session_maker() as s:
        try:
            for quality_data in data['qualities']:
                await Quality.create(QualityCreateSchema(resolution=quality_data['resolution']).model_dump(), s)
        finally:
            await s.close()


async def create_movies_from_json(data):
    async with session_maker() as s:
        try:
            for movie_data in data['movies']:
                await Movie.create(
                    MovieCreateSchema(
                        original_title=movie_data['original_title'],
                        translated_title=movie_data['translated_title'],
                        poster=movie_data['poster'],
                        description=movie_data['description'],
                        age_id=movie_data['age_id'],
                        category_id=movie_data['category_id']
                    ).model_dump(),
                    s,
                )
        finally:
            await s.close()


async def create_seasons_from_json(data):
    async with session_maker() as s:
        try:
            for season_data in data['seasons']:
                await Season.create(
                    SeasonCreateSchema(
                        number=season_data['number'],
                        movie_id=season_data['movie_id']
                    ).model_dump(),
                    s,
                )
        finally:
            await s.close()


async def create_episodes_from_json(data):
    async with session_maker() as s:
        try:
            for episode_data in data['episodes']:
                await Episode.create(
                    EpisodeCreateSchema(
                        number=episode_data['number'],
                        season_id=episode_data['season_id'],
                        title=episode_data['title'],
                        release_date=datetime.datetime.strptime(episode_data['release_date'], '%Y-%m-%d')
                    ).model_dump(),
                    s,
                )
        finally:
            await s.close()


async def create_records_from_json(data):
    async with session_maker() as s:
        try:
            for record_data in data['records']:
                await Record.create(
                    RecordCreateSchema(
                        episode_id=record_data['episode_id'],
                        quality_id=record_data['quality_id'],
                        filename=record_data['filename']
                    ).model_dump(),
                    s,
                )
        finally:
            await s.close()


async def create_screenshots_from_json(data):
    async with session_maker() as s:
        try:
            for screenshot_data in data['screenshots']:
                await Screenshot.create(
                    ScreenshotCreateSchema(
                        filename=screenshot_data['filename'],
                        title=screenshot_data['title'],
                        movie_id=screenshot_data['movie_id'],
                    ).model_dump(),
                    s,
                )
        finally:
            await s.close()


async def create_tags_from_json(data):
    async with session_maker() as s:
        try:
            for tag_data in data['tags']:
                await Tag.create(TagCreateSchema(title=tag_data['title']).model_dump(), s)
        finally:
            await s.close()


async def create_taggings_from_json(data):
    async with session_maker() as s:
        try:
            for tagging_data in data['taggings']:
                await Tagging.create(
                    TaggingCreateSchema(
                        movie_id=tagging_data['movie_id'],
                        tag_id=tagging_data['tag_id']
                    ).model_dump(),
                    s
                )
        finally:
            await s.close()


async def create_genres_from_json(data):
    async with session_maker() as s:
        try:
            for genre_data in data['genres']:
                await Genre.create(GenreCreateSchema(title=genre_data['title']).model_dump(), s)
        finally:
            await s.close()


async def create_movies_genres_from_json(data):
    async with session_maker() as s:
        try:
            for movie_genre_data in data['movies_genres']:
                await MovieGenre.create(
                    MovieGenreCreateSchema(
                        movie_id=movie_genre_data['movie_id'],
                        genre_id=movie_genre_data['genre_id']
                    ).model_dump(),
                    s
                )
        finally:
            await s.close()


async def create_persons(data):
    async with session_maker() as s:
        try:
            for person_data in data['persons']:
                await Person.create(PersonCreateSchema(name=person_data['name']).model_dump(), s)
        finally:
            await s.close()


async def create_activities(data):
    async with session_maker() as s:
        try:
            for activity_data in data['activities']:
                await Activity.create(ActivityCreateSchema(title=activity_data['title']).model_dump(), s)
        finally:
            await s.close()


async def create_movies_persons(data):
    async with session_maker() as s:
        try:
            for movie_person_data in data['movies_persons']:
                await MoviePerson.create(
                    MoviePersonCreateSchema(
                        movie_id=movie_person_data['movie_id'],
                        person_id=movie_person_data['person_id'],
                        activity_id=movie_person_data['activity_id']
                    )
                    .model_dump(),
                    s
                )
        finally:
            await s.close()


async def init():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    await create_ages_from_json(data)
    await create_categories_from_json(data)
    await create_qualities_from_json(data)
    await create_movies_from_json(data)
    await create_seasons_from_json(data)
    await create_episodes_from_json(data)
    await create_records_from_json(data)
    await create_screenshots_from_json(data)
    await create_tags_from_json(data)
    await create_taggings_from_json(data)
    await create_genres_from_json(data)
    await create_movies_genres_from_json(data)
    await create_persons(data)
    await create_activities(data)
    await create_movies_persons(data)


asyncio.run(init())
