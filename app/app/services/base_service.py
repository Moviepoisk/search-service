from typing import Type, Optional, List
from pydantic import BaseModel, parse_obj_as
import orjson
from app.services.cache_manager import CacheManager
from app.services.elasticsearch_service import ElasticsearchService


class BaseService:
    def __init__(self, cache_manager: CacheManager, es_service: ElasticsearchService, index_name: str):
        self.cache_manager = cache_manager
        self.es_service = es_service
        self.index_name = index_name

    async def _get_by_id(self, item_id: str, model: Type[BaseModel]) -> Optional[BaseModel]:
        cache_key = self.cache_manager.generate_cache_key(self.index_name, item_id)
        item = await self._get_from_cache(cache_key, model)
        if not item:
            item = await self._get_from_elastic(item_id, model)
            if item:
                await self._put_to_cache(cache_key, [item])  # Put single item in a list
        return item

    async def _search(self, query: str, page: int, size: int, model: Type[BaseModel]) -> List[BaseModel]:
        cache_key = self.cache_manager.generate_cache_key(
            self.index_name, 'search', query, page, size)
        cached_results = await self._get_from_cache(cache_key, model)
        if cached_results:
            return cached_results

        start = (page - 1) * size
        results = await self.es_service.custom_search(self.index_name, query, start, size)
        await self._put_to_cache(cache_key, [model(**hit) for hit in results])
        return [model(**hit) for hit in results]

    async def _search_field(self, field_search: str,
                            query: str, page: int, size: int, model: Type[BaseModel]) -> List[BaseModel]:
        cache_key = self.cache_manager.generate_cache_key(
            self.index_name, 'search_field', field_search, query, page, size)
        cached_results = await self._get_from_cache(cache_key, model)
        if cached_results:
            return cached_results

        start = (page - 1) * size
        results = await self.es_service.search_field(self.index_name, field_search, query, start, size)
        await self._put_to_cache(cache_key, [model(**hit) for hit in results])
        return [model(**hit) for hit in results]

    async def _get_from_elastic(self, item_id: str, model: Type[BaseModel]) -> Optional[BaseModel]:
        result = await self.es_service.get_by_id(self.index_name, item_id)
        if result:
            return model(**result)
        return None

    async def _get_from_cache(self, key: str, model: Type[BaseModel]) -> List[BaseModel]:
        data = await self.cache_manager.get(key)
        if data:
            items = orjson.loads(data)
            return [parse_obj_as(model, item) for item in items]
        return []

    async def _put_to_cache(self, key: str, items: List[BaseModel]):
        data = orjson.dumps([item.dict() for item in items])
        await self.cache_manager.set(key, data)
