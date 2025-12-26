from fastapi import APIRouter
from fastapi.params import Depends
from uuid import UUID

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.blog.dto import BlogCreateDto, BlogGetDto, BlogUpdateDto
from app.features.blog.service import (
    BlogSortField,
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[BlogGetDto],
    tags=["blog"],
    summary="Find Blog",
)
async def get_all_blog( 
    search: str | None = None,
    sort_by: BlogSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),):
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
    response_model=BlogGetDto,
    tags=["blog"],
    summary="Find Blog by id",
)
async def get_blog_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["blog"],
    summary="Create Blog",
    dependencies=[Depends(require_admin)]
)
async def create_blog(
    blog: BlogCreateDto, 
    db: Session = Depends(get_db),
):
    return create(db, blog)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["blog"],
    summary="Update Blog",
    dependencies=[Depends(require_admin)]
)
async def update_blog(id: UUID, blog: BlogUpdateDto, db: Session = Depends(get_db)):
    return update_by_id(db, id, blog)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["blog"],
    summary="Delete Blog",
    dependencies=[Depends(require_admin)]
)
async def delete_blog(id: UUID, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
