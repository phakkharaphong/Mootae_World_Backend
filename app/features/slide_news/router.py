from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.slide_news.dto import (
    SlideNewCreateDto,
    SlideNewGetDto,
    SlideNewUpdateDto,
)
from app.features.slide_news.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


router = APIRouter(
    prefix="/slide-new",
    tags=["slide-new"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[SlideNewGetDto],
    tags=["slide-new"],
    summary="Find Slide New",
)
async def get_all_slide_news(
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=SlideNewGetDto,
    tags=["slide-new"],
    summary="Find Slide New by id",
)
async def get_slide_news_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["slide-new"],
    summary="Create Slide News",
)
async def create_slide_news(slide_news: SlideNewCreateDto, db: Session = Depends(get_db)):
    return create(db, slide_news)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["slide-new"],
    summary="Update Slide New",
)
async def update_slide_news(
    id: str, slide_news: SlideNewUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, slide_news)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["slide-new"],
    summary="Delete Slide News",
)
async def delete_slide_news(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
