from abc import ABC, abstractmethod
from typing import List, Optional
from elasticsearch import AsyncElasticsearch, NotFoundError


NESTED_FIELDS = ["actors.name", "directors.name", "writers.name"]

class ElasticsearchService(ABC):
    @abstractmethod
    async def get_by_id(self, index_name: str, item_id: str) -> Optional[dict]:
        pass


    @abstractmethod
    async def custom_search(self, index_name: str, query: str, start: int, size: int) -> List[dict]:
        pass

    @abstractmethod
    async def search_field(
        self, index_name: str, field_search: str, query: str, start: int, size: int
        ) -> List[dict]:
        pass


class AsyncElasticsearchService(ElasticsearchService):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic


    async def get_by_id(self, index_name: str, item_id: str) -> Optional[dict]:
        try:
            response = await self.elastic.get(index=index_name, id=item_id)
            return response["_source"]
        except NotFoundError:
            return None


    async def custom_search(self, index_name: str, query: str, start: int, size: int) -> List[dict]:
        search_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["*"],
                }
            },
            "from": start,
            "size": size
        }
        response = await self.elastic.search(index=index_name, body=search_query)
        return [hit["_source"] for hit in response["hits"]["hits"]]


    async def search_field(self, index_name: str, field_search: str, query: str, start: int, size: int) -> List[dict]:
        if field_search in NESTED_FIELDS:
            search_query = {
                "query": {
                    "nested": {
                        "path": field_search.split(".")[0],
                        "query": {"match": {field_search: query}},
                    }
                },
                "from": start,
                "size": size
            }
        else:
            search_query = {
                "query": {"fuzzy": {field_search: query}},
                "from": start,
                "size": size
            }
        response = await self.elastic.search(index=index_name, body=search_query)
        return [hit["_source"] for hit in response["hits"]["hits"]]
