from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from app.features.blog_homepage.dto import (
    BlogHomePageCreateDto,
    BlogHomePageGetDto,
    BlogHomePageUpdateDto,
)
from sqlalchemy.orm import Session
from app.features.blog_homepage.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


router = APIRouter(
    prefix="/blog-homepage",
    tags=["blog-homepage"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[BlogHomePageGetDto],
    tags=["blog-homepage"],
    summary="Find Blog home page",
)
async def get_all_blog_homepage(
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=BlogHomePageGetDto,
    tags=["blog-homepage"],
    summary="Find Blog home page by id",
)
async def get_blog_homepage_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["blog-homepage"],
    summary="Create Blog home page",
)
async def create_blog_homepage(
    blog_homepage: BlogHomePageCreateDto, db: Session = Depends(get_db)
):
    return create(db, blog_homepage)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["blog-homepage"],
    summary="Update Blog home page",
)
async def update_blog_homepage(
    id: str, blog_homepage: BlogHomePageUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, blog_homepage)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["blog-homepage"],
    summary="Delete Blog home page",
)
async def delete_blog_homepage(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
