from typing import Optional
from app.interfaces.igenre_service import IGenreService
from app.services.base_service import BaseService
from app.models.genre import Genre
from app.services.cache_manager import CacheManager
from app.services.elasticsearch_service import ElasticsearchService

class GenreService(BaseService, IGenreService):
    def __init__(self, cache_manager: CacheManager, es_service: ElasticsearchService):
        super().__init__(cache_manager, es_service, 'genres')

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        return await self._get_by_id(genre_id, Genre)

    async def search_genres(self, query: str, page: int, size: int) -> list[Genre]:
        return await self._search(query, page, size, Genre)

    async def search_genres_by_field(self, field_search: str, query: str, page: int, size: int) -> list[Genre]:
        return await self._search_field(field_search, query, page, size, Genre)