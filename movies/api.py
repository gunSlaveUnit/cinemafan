from fastapi import APIRouter

from movies.models import Movie, Episode, Quality, Record
from movies.schemas import MovieCreateSchema, EpisodeCreateSchema, QualityCreateSchema, RecordCreateSchema
from root.crud import crud

movies_api_router = APIRouter()

movies_router = APIRouter(prefix="/movies", tags=["Movies"])
crud(movies_router, Movie, MovieCreateSchema)
movies_api_router.include_router(movies_router)

episodes_router = APIRouter(prefix="/episodes", tags=["Episodes"])
crud(episodes_router, Episode, EpisodeCreateSchema)
movies_api_router.include_router(episodes_router)

qualities_router = APIRouter(prefix="/qualities", tags=["Qualities"])
crud(qualities_router, Quality, QualityCreateSchema)
movies_api_router.include_router(qualities_router)

records_router = APIRouter(prefix="/records", tags=["Records"])
crud(records_router, Record, RecordCreateSchema)
movies_api_router.include_router(records_router)
