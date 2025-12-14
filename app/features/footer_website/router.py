from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.footer_website.dto import (
    FooterWebsiteCreateDto,
    FooterWebsiteGetDto,
    FooterWebsiteUpdateDto,
)
from app.features.footer_website.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


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
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=FooterWebsiteGetDto,
    tags=["footer-website"],
    summary="Find Footer Website by id",
)
async def get_footer_website_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["footer-website"],
    summary="Create Footer Website",
)
async def create_footer_website(
    footer_website: FooterWebsiteCreateDto, db: Session = Depends(get_db)
):
    return create(db, footer_website)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["footer-website"],
    summary="Update Footer Website",
)
async def update_footer_website(
    id: str, footer_website: FooterWebsiteUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, footer_website)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["footer-website"],
    summary="Delete Footer Website",
)
async def delete_footer_website(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
