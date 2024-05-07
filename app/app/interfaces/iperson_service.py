from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.person import Person

class IPersonService(ABC):

    @abstractmethod
    async def get_by_id(self, film_id: str) -> Optional[Person]:
        pass

    @abstractmethod
    async def search_persons(self, query: str, page: int, size: int) -> List[Person]:
        pass

    @abstractmethod
    async def search_persons_by_field(self, field_search: str, query: str, page: int, size: int) -> List[Person]:
        pass
