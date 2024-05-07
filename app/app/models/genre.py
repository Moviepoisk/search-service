from uuid import UUID
from app.models.common import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    id: UUID
    name: str
    description: str | None
