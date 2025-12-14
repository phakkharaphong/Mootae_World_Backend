from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.promotion.dto import (
    PromotionCreateDto,
    PromotionGetDto,
    PromotionUpdateDto,
)
from app.features.promotion.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


router = APIRouter(
    prefix="/promotion",
    tags=["promotion"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[PromotionGetDto],
    tags=["promotion"],
    summary="Find Promotion",
)
async def get_all_category(
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=PromotionGetDto,
    tags=["promotion"],
    summary="Find Promotion by id",
)
async def get_promotion_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["promotion"],
    summary="Create Promotion",
)
async def create_promotion(
    promotion: PromotionCreateDto, db: Session = Depends(get_db)
):
    return create(db, promotion)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["promotion"],
    summary="Update Promotion",
)
async def update_promotion(
    id: str, promotion: PromotionUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, promotion)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["promotion"],
    summary="Delete Promotion",
)
async def delete_promotion(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
