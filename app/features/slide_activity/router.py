from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.slide_activity.dto import (
    SlideActivityCreateDto,
    SlideActivityGetDto,
    SlideActivityUpdateDto,
)
from app.features.slide_activity.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseModel


router = APIRouter(
    prefix="/slide-activity",
    tags=["slide-activity"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[SlideActivityGetDto],
    tags=["slide-activity"],
    summary="Find Slide Activity",
)
async def get_all_slide_activity(
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=SlideActivityGetDto,
    tags=["slide-activity"],
    summary="Find Slide Activity by id",
)
async def get_slide_activity_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["slide-activity"],
    summary="Create Slide Activity",
)
async def create_slide_activity(
    slide_activity: SlideActivityCreateDto, db: Session = Depends(get_db)
):
    return create(db, slide_activity)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["slide-activity"],
    summary="Update Slide Activity",
)
async def update_slide_activity(
    id: str, slide_activity: SlideActivityUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, slide_activity)


@router.delete(
    "/{id}",
    response_model=ResponseModel,
    tags=["slide-activity"],
    summary="Delete Slide Activity",
)
async def delete_slide_activity(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
