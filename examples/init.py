import asyncio
import json

from movies.models import Age, Movie, Episode, Quality, Record, Category, Season, Screenshot, Tag, Tagging, Genre, \
    MovieGenre, Person, Activity, MoviePerson, Studio, MovieStudio
from infrastructure.db import session_maker
from movies.schemas import AgeCreateSchema, MovieCreateSchema, EpisodeCreateSchema, QualityCreateSchema, \
    RecordCreateSchema, CategoryCreateSchema, SeasonCreateSchema, ScreenshotCreateSchema, TagCreateSchema, \
    TaggingCreateSchema, GenreCreateSchema, MovieGenreCreateSchema, MoviePersonCreateSchema, PersonCreateSchema, \
    ActivityCreateSchema, StudioCreateSchema, MovieStudioCreateSchema


async def init():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        async with session_maker() as s:
            try:
                ages = data['ages']
                for age in ages:
                    await Age.create(AgeCreateSchema(**age).model_dump(), s)

                categories = data['categories']
                for category in categories:
                    await Category.create(CategoryCreateSchema(**category).model_dump(), s)

                qualities = data['qualities']
                for quality in qualities:
                    await Quality.create(QualityCreateSchema(**quality).model_dump(), s)

                records = data['records']
                for record in records:
                    await Record.create(RecordCreateSchema(**record).model_dump(), s)

                screenshots = data['screenshots']
                for screenshot in screenshots:
                    await Screenshot.create(ScreenshotCreateSchema(**screenshot).model_dump(), s)

                tags = data['tags']
                for tag in tags:
                    await Tag.create(TagCreateSchema(**tag).model_dump(), s)

                taggings = data['taggings']
                for tagging in taggings:
                    await Tagging.create(TaggingCreateSchema(**tagging).model_dump(), s)

                genres = data['genres']
                for genre in genres:
                    await Genre.create(GenreCreateSchema(**genre).model_dump(), s)

                movies_genres = data['movies_genres']
                for movie_genre in movies_genres:
                    await MovieGenre.create(MovieGenreCreateSchema(**movie_genre).model_dump(), s)

                persons = data['persons']
                for person in persons:
                    await Person.create(PersonCreateSchema(**person).model_dump(), s)

                activities = data['activities']
                for activity in activities:
                    await Activity.create(ActivityCreateSchema(**activity).model_dump(), s)

                movies_persons = data['movies_persons']
                for movie_person in movies_persons:
                    await MoviePerson.create(MoviePersonCreateSchema(**movie_person).model_dump(), s)

                studios = data['studios']
                for studio in studios:
                    await Studio.create(StudioCreateSchema(**studio).model_dump(), s)

                movies_studios = data['movies_studios']
                for movie_studio in movies_studios:
                    await MovieStudio.create(MovieStudioCreateSchema(**movie_studio).model_dump(), s)

                movies = data['movies']
                for movie in movies:
                    await Movie.create(MovieCreateSchema(**movie).model_dump(), s)

                seasons = data['seasons']
                for season in seasons:
                    await Season.create(SeasonCreateSchema(**season).model_dump(), s)

                episodes = data['episodes']
                for episode in episodes:
                    await Episode.create(EpisodeCreateSchema(**episode).model_dump(), s)
            finally:
                await s.close()


asyncio.run(init())
