from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.blog.dto import BlogCreateDto, BlogGetDto, BlogUpdateDto
from app.features.blog.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


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
async def get_all_blog(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=BlogGetDto,
    tags=["blog"],
    summary="Find Blog by id",
)
async def get_blog_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["blog"],
    summary="Create Blog",
)
async def create_blog(blog: BlogCreateDto, db: Session = Depends(get_db)):
    return create(db, blog)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["blog"],
    summary="Update Blog",
)
async def update_blog(id: str, blog: BlogUpdateDto, db: Session = Depends(get_db)):
    return update_by_id(db, id, blog)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["blog"],
    summary="Delete Blog",
)
async def delete_blog(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
