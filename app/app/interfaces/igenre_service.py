from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.genre import Genre

class IGenreService(ABC):

    @abstractmethod
    async def get_by_id(self, film_id: str) -> Optional[Genre]:
        pass

    @abstractmethod
    async def search_genres(self, query: str, page: int, size: int) -> List[Genre]:
        pass

    @abstractmethod
    async def search_genres_by_field(self, field_search: str, query: str, page: int, size: int) -> List[Genre]:
        pass
