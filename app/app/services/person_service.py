from typing import Optional
from app.interfaces.iperson_service import IPersonService
from app.services.base_service import BaseService
from app.models.person import Person
from app.services.cache_manager import CacheManager
from app.services.elasticsearch_service import ElasticsearchService

class PersonService(BaseService, IPersonService):
    def __init__(self, cache_manager: CacheManager, es_service: ElasticsearchService):
        super().__init__(cache_manager, es_service, 'persons')

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        return await self._get_by_id(person_id, Person)

    async def search_persons(self, query: str, page: int, size: int) -> list[Person]:
        return await self._search(query, page, size, Person)

    async def search_persons_by_field(self, field_search: str, query: str, page: int, size: int) -> list[Person]:
        return await self._search_field(field_search, query, page, size, Person)
