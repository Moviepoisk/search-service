from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.film import Film
from app.interfaces.ifilm_service import IFilmService
from app.services.dependencies import get_film_service
from search.app.app.api.common import PaginatedParams

router = APIRouter()


class InvalidFieldNameError(Exception):
    pass


@router.get("/{film_id}", response_model=Film, summary="Get Film Details")
async def film_details(
    film_id: str, _service: IFilmService = Depends(get_film_service)
) -> Film:
    """
    Retrieve detailed information about a film by its ID.
    - **film_id**: UUID of the film to retrieve details for.
    """
    film = await _service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return film


@router.get("/search/", response_model=list[Film], summary="Search Films by Query Params")
async def search_films(
    query: str = Query(None, min_length=1, description="Search query string"),
    paginated_params: PaginatedParams = Depends(),
    _service: IFilmService = Depends(get_film_service)
) -> list[Film]:
    """
    Search for films based on a query string with pagination.
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    if not query:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Query string is required")
    films = await _service.search_films(query, paginated_params.page, paginated_params.size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films not found")
    return films


@router.get(
    "/search_field/",
    response_model=list[Film],
    summary="Search Films by Field",
)
async def search_field(
    field_search: str = Query(...,
                              description="Field to search in, e.g., 'title', 'genre', 'actors.name'"),
    query: str = Query(..., description="Search query string"),
    paginated_params: PaginatedParams = Depends(),
    _service: IFilmService = Depends(get_film_service),
) -> list[Film]:
    """
    Search for films based on a specified field and query with pagination.
    - **field_search**: The field to search in (e.g., 'title', 'genre', 'actors.name').
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    if not query:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Query string is required")
    if not field_search:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Field search is required")
    try:
        films = await _service.search_films_by_field(field_search, query, paginated_params.page, paginated_params.size)
    except InvalidFieldNameError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No films found matching the query")
    return films
