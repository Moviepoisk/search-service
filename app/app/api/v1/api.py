from fastapi import APIRouter

from app.api.v1 import persons, genres, movies


api_router = APIRouter()
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
