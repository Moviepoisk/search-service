from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.film import Film
from app.services.film_service import FilmService
from app.services.dependencies import get_film_service

router = APIRouter()

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1


class InvalidFieldNameError(Exception):
    pass


@router.get("/{film_id}", response_model=Film, summary="Get Film Details")
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    """
    Retrieve detailed information about a film by its ID.
    - **film_id**: UUID of the film to retrieve details for.
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return film


@router.get("/search/{query}", response_model=list[Film], summary="Search Films")
async def search_films(
    query: str,
    page: int = Query(DEFAULT_PAGE_NUMBER, alias="page", description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page"),
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:
    """
    Search for films based on a query string with pagination.
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    films = await film_service._search(query, page, size, Film)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films not found")
    return films


@router.get(
    "/search_field/{field_search}/{query}",
    response_model=list[Film],
    summary="Search Films by Field",
)
async def search_field(
    field_search: str = Query(...,
                              description="Field to search in, e.g., 'title', 'genre', 'actors.name'"),
    query: str = Query(..., description="Search query string"),
    page: int = Query(DEFAULT_PAGE_NUMBER, alias="page", description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page"),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    """
    Search for films based on a specified field and query with pagination.
    - **field_search**: The field to search in (e.g., 'title', 'genre', 'actors.name').
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    try:
        films = await film_service._search_field(field_search, query, page, size, Film)
    except InvalidFieldNameError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="No films found matching the query"
        )

    return films
