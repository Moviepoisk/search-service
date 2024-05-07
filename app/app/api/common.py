from pydantic import BaseModel, Field

DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_NUMBER = 1


class PaginatedParams(BaseModel):
    page: int = Field(DEFAULT_PAGE_NUMBER, alias="page", description="Page number")
    size: int = Field(DEFAULT_PAGE_SIZE, alias="size",
                      description="Number of results per page")
