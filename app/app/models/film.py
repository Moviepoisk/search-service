from uuid import UUID
from app.models.common import BaseOrjsonModel


class Person(BaseOrjsonModel):
    name: str | None


class Film(BaseOrjsonModel):
    id: UUID
    imdb_rating: float | None
    genre: list[str] | None
    title: str
    description: str | None
    type: str | None
    actors: list[Person] | None
    directors: list[Person] | None
    writers: list[Person] | None
