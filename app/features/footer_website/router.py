from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.footer_website.dto import (
    FooterWebsiteCreateDto,
    FooterWebsiteGetDto,
    FooterWebsiteUpdateDto,
)
from app.features.footer_website.service import (
    FooterSortField,
    find_all,
    find_by_id,
    create,
    update,
    delete,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


router = APIRouter(
    prefix="/footer-website",
    tags=["footer-website"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[FooterWebsiteGetDto],
    tags=["footer-website"],
    summary="Find Footer Website",
)
async def get_all_footer_website(
    search: str | None = None,
    sort_by: FooterSortField | None = "created_at",
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
    response_model=FooterWebsiteGetDto,
    tags=["footer-website"],
    summary="Find Footer Website by id",
)
async def get_footer_website_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["footer-website"],
    summary="Create Footer Website",
    dependencies=[Depends(require_admin)]
)
async def create_footer_website(
    footer_website: FooterWebsiteCreateDto, 
    db: Session = Depends(get_db)
):
    return create(db, footer_website)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["footer-website"],
    summary="Update Footer Website",
    dependencies=[Depends(require_admin)]
)
async def update_footer_website(
    id: UUID, 
    footer_website: FooterWebsiteUpdateDto, 
    db: Session = Depends(get_db)
):
    return update(db, id, footer_website)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["footer-website"],
    summary="Delete Footer Website",
    dependencies=[Depends(require_admin)]
)
async def delete_footer_website(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return delete(db, id)
