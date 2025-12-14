from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.category.dto import (
    CategoryCreateDto,
    CategoryGetDto,
    CategoryUpdateDto,
)
from app.features.category.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[CategoryGetDto],
    tags=["category"],
    summary="Find Category",
)
async def get_all_category(
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=CategoryGetDto,
    tags=["category"],
    summary="Find Category by id",
)
async def get_category_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["category"],
    summary="Create Category",
)
async def create_category(category: CategoryCreateDto, db: Session = Depends(get_db)):
    return create(db, category)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["category"],
    summary="Update Category",
)
async def update_category(
    id: str, category: CategoryUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, category)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["category"],
    summary="Delete Category",
)
async def delete_category(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
