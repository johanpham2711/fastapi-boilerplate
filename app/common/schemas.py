from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    success: bool = True
    code: int = 200
    message: str = "Success"
    data: T | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    code: int
    message: str
    errors: Any | None = None


class PaginationResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    total_pages: int

    @classmethod
    def create(cls, items: list[T], total: int, page: int, limit: int):
        total_pages = (total + limit - 1) // limit if limit > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )

