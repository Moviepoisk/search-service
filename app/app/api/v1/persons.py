from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.person import Person
from app.interfaces.iperson_service import IPersonService
from app.services.dependencies import get_person_service
from search.app.app.api.common import PaginatedParams

router = APIRouter()


class InvalidFieldNameError(Exception):
    pass


@router.get("/{_id}", response_model=Person, summary="Get Person Details")
async def person_details(
    _id: str, _service: IPersonService = Depends(get_person_service)
) -> Person:
    """
    Retrieve detailed information about a person by its ID.
    - **_id**: UUID of the person to retrieve details for.
    """
    result = await _service.get_by_id(_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return result


@router.get("/search/", response_model=list[Person], summary="Search Persons")
async def search_persons(
    query: str = Query(None, min_length=1, description="Search query string"),
    paginated_params: PaginatedParams = Depends(),
    _service: IPersonService = Depends(get_person_service)
) -> list[Person]:
    """
    Search for persons based on a query string with pagination.
    - **query**: The search query string.
    - **paginated_params**: Pagination parameters.
    """
    result = await _service.search_persons(query, paginated_params.page, paginated_params.size)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Persons not found")
    return result


@router.get(
    "/search_field/",
    response_model=list[Person],
    summary="Search Persons by Field",
)
async def search_field(
    field_search: str = Query(...,
                              description="Field to search in, e.g., 'title', 'genre', 'actors.name'"),
    query: str = Query(..., description="Search query string"),
    paginated_params: PaginatedParams = Depends(),
    _service: IPersonService = Depends(get_person_service),
) -> list[Person]:
    """
    Search for persons based on a specified field and query with pagination.
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
        result = await _service.search_persons_by_field(field_search, query, paginated_params.page,
                                                        paginated_params.size)
    except InvalidFieldNameError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="No persons found matching the query"
        )

    return result
