from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query
from models.person import Person
from services.person_service import PersonService
from app.services.dependencies import get_person_service

router = APIRouter()

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1


class InvalidFieldNameError(Exception):
    pass


@router.get("/{_id}", response_model=Person, summary="Get Person Details")
async def person_details(
    _id: str, _service: PersonService = Depends(get_person_service)
) -> Person:
    """
    Retrieve detailed information about a person by its ID.
    - **_id**: UUID of the person to retrieve details for.
    """
    result = await _service.get_by_id(_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return result


@router.get("/search/{query}", response_model=list[Person], summary="Search Persons")
async def search_persons(
    query: str,
    page: int = Query(DEFAULT_PAGE_NUMBER, alias="page", description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page"),
    _service: PersonService = Depends(get_person_service)
) -> list[Person]:
    """
    Search for persons based on a query string with pagination.
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    result = await _service.search_persons(query, page, size)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Persons not found")
    return result


@router.get(
    "/search_field/{field_search}/{query}",
    response_model=list[Person],
    summary="Search Persons by Field",
)
async def search_field(
    field_search: str = Query(...,
                              description="Field to search in, e.g., 'title', 'genre', 'actors.name'"),
    query: str = Query(..., description="Search query string"),
    page: int = Query(DEFAULT_PAGE_NUMBER, alias="page", description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page"),
    _service: PersonService = Depends(get_person_service),
) -> list[Person]:
    """
    Search for persons based on a specified field and query with pagination.
    - **field_search**: The field to search in (e.g., 'title', 'genre', 'actors.name').
    - **query**: The search query string.
    - **page**: Page number.
    - **size**: Number of results per page.
    """
    try:
        result = await _service.search_persons_by_field(field_search, query, page, size)
    except InvalidFieldNameError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="No persons found matching the query"
        )

    return result
