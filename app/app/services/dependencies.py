from functools import lru_cache
from fastapi import Depends
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from app.services.elasticsearch_service import AsyncElasticsearchService, ElasticsearchService
from app.services.film_service import FilmService
from app.services.genre_service import GenreService
from app.services.person_service import PersonService
from app.services.cache_manager import CacheManager, RedisCacheManager
from app.db.elastic import get_elastic
from app.db.redis import get_redis

@lru_cache()
def get_redis_cache_manager(redis: Redis = Depends(get_redis)) -> RedisCacheManager:
    return RedisCacheManager(redis)

@lru_cache()
def get_elasticsearch_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)) -> ElasticsearchService:
    return AsyncElasticsearchService(elastic)

@lru_cache()
def get_film_service(
    cache_manager: CacheManager = Depends(get_redis_cache_manager),
    es_service: ElasticsearchService = Depends(get_elasticsearch_service),
) -> FilmService:
    return FilmService(cache_manager, es_service)

@lru_cache()
def get_genre_service(
    cache_manager: CacheManager = Depends(get_redis_cache_manager),
    es_service: ElasticsearchService = Depends(get_elasticsearch_service),
) -> GenreService:
    return GenreService(cache_manager, es_service)

@lru_cache()
def get_person_service(
    cache_manager: CacheManager = Depends(get_redis_cache_manager),
    es_service: ElasticsearchService = Depends(get_elasticsearch_service),
) -> PersonService:
    return PersonService(cache_manager, es_service)
