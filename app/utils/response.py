from typing import Any, Generic, List, TypeVar
from pydantic import BaseModel
from uuid import UUID
T = TypeVar("T")


class Pagination(BaseModel):
    page: int
    limit: int
    total: int


class PaginatedResponse(BaseModel, Generic[T]):
    message: str
    data: List[T]
    pagination: Pagination


class ResponseModel(BaseModel):
    status: int
    message: str
    data: Any


class ResponseDeleteModel(BaseModel):
    status: int
    message: str
    data: UUID


class ResponseByIdModel(BaseModel, Generic[T]):
    status: int
    message: str
    data: List[T]


class ResponseBiModel(BaseModel, Generic[T]):
    message: str
    data: List[T]
