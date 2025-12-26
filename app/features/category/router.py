from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import delete, update

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.category.dto import (
    CategoryCreateDto,
    CategoryGetDto,
    CategoryUpdateDto,
)
from app.features.category.service import (
    CategorySortField,
    find_all,
    find_by_id,
    create,
    update,
    delete
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


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
    search: str | None = None,
    sort_by: CategorySortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return find_all(   
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        is_active=is_active,
        page=page,
        limit=limit,
        )


@router.get(
    "/{id}",
    response_model=CategoryGetDto,
    tags=["category"],
    summary="Find Category by id",
)
async def get_category_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["category"],
    summary="Create Category",
    dependencies=[Depends(require_admin)]
)
async def create_category(category: CategoryCreateDto, db: Session = Depends(get_db)):
    return create(db, category)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["category"],
    summary="Update Category",
    dependencies=[Depends(require_admin)]
)
async def update_category(
    id: UUID, category: CategoryUpdateDto, db: Session = Depends(get_db)
):
    return update(db, id, category)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["category"],
    summary="Delete Category",
    dependencies=[Depends(require_admin)]
)
async def delete_category(id: UUID, db: Session = Depends(get_db)):
    return delete(db, id)
