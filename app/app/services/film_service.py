from typing import Optional
from app.services.base_service import BaseService
from app.interfaces.ifilm_service import IFilmService
from app.models.film import Film
from app.services.cache_manager import CacheManager
from app.services.elasticsearch_service import ElasticsearchService

class FilmService(BaseService, IFilmService):
    def __init__(self, cache_manager: CacheManager, es_service: ElasticsearchService):
        super().__init__(cache_manager, es_service, 'movies')

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        return await self._get_by_id(film_id, Film)

    async def search_films(self, query: str, page: int, size: int) -> list[Film]:
        return await self._search(query, page, size, Film)

    async def search_films_by_field(self, field_search: str, query: str, page: int, size: int) -> list[Film]:
        return await self._search_field(field_search, query, page, size, Film)
