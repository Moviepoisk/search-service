from uuid import UUID
from app.models.common import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: UUID
    full_name: str
    role: list[str] | None
    films_id: list[UUID] | None
