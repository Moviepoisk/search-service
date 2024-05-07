from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.film import Film

class IFilmService(ABC):

    @abstractmethod
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        pass

    @abstractmethod
    async def search_films(self, query: str, page: int, size: int) -> List[Film]:
        pass

    @abstractmethod
    async def search_films_by_field(self, field_search: str, query: str, page: int, size: int) -> List[Film]:
        pass
