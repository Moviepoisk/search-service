from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.genre import Genre
from app.services.genre_service import GenreService
from app.services.dependencies import get_genre_service

router = APIRouter()

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1


class InvalidFieldNameError(Exception):
    pass


@router.get("/{_id}", response_model=Genre, summary="Get Genre Details")
async def genre_details(_id: str, _service: GenreService = Depends(get_genre_service)
                        ) -> Genre:
    """
    Retrieve detailed information about a genre by its ID.
    - **_id**: UUID of the genre to retrieve details for.
    """
    result = await _service.get_by_id(_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")
    return result


@router.get("/search/{query}", response_model=list[Genre], summary="Search Genres")
async def search_genres(
    query: str,
    page: int = Query(DEFAULT_PAGE_NUMBER, alias="page", description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page"),
    _service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """
    Search for genres based on a query string with pagination.
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    result = await _service.search_genres(query, page, size)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres not found")
    return result


@router.get(
    "/search_field/{field_search}/{query}",
    response_model=list[Genre],
    summary="Search Genres by Field",
)
async def search_field(
    field_search: str = Query(..., description="Field to search in, e.g., 'full_name'"),
    query: str = Query(..., description="Search query string"),
    page: int = Query(DEFAULT_PAGE_NUMBER, alias="page", description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page"),
    _service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    """
    Search for genres based on a specified field and query with pagination.
    - **field_search**: The field to search in (e.g., 'name').
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    try:
        result = await _service.search_genres_by_field(field_search, query, page, size)
    except InvalidFieldNameError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="No genres found matching the query"
        )

    return result
