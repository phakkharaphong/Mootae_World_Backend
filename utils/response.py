from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel

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
    data: str