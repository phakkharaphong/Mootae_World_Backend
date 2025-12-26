from fastapi import APIRouter
from fastapi.params import Depends
from uuid import UUID
from app.core.database import get_db
from app.features.auth.router import require_admin
from app.features.blog_homepage.dto import (
    BlogHomePageCreateDto,
    BlogHomePageGetDto,
    BlogHomePageUpdateDto,
)
from sqlalchemy.orm import Session
from app.features.blog_homepage.service import (
    BlogHomepageSortField,
    find_all,
    find_by_id,
    create,
    update,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


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
    search: str | None = None,
    sort_by: BlogHomepageSortField | None = "created_at",
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
    response_model=BlogHomePageGetDto,
    tags=["blog-homepage"],
    summary="Find Blog home page by id",
)
async def get_blog_homepage_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["blog-homepage"],
    summary="Create Blog home page",
    dependencies=[Depends(require_admin)]
)
async def create_blog_homepage(
    blog_homepage: BlogHomePageCreateDto, 
    db: Session = Depends(get_db)
):
    return create(db, blog_homepage)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["blog-homepage"],
    summary="Update Blog home page",
    dependencies=[Depends(require_admin)]
)
async def update_blog_homepage(
    id: UUID, 
    blog_homepage: BlogHomePageUpdateDto, 
    db: Session = Depends(get_db)
):
    return update(db, id, blog_homepage)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["blog-homepage"],
    summary="Delete Blog home page",
    dependencies=[Depends(require_admin)]
)
async def delete_blog_homepage(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return delete_by_id(db, id)
