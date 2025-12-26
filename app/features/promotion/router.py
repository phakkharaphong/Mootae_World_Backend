from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.promotion.dto import (
    PromotionCreateDto,
    PromotionGetDto,
    PromotionUpdateDto,
)
from app.features.promotion.service import (
    PromotionSortField,
    find_all,
    find_by_id,
    create,
    update,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


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
    search: str | None = None,
    sort_by: PromotionSortField | None = "created_at",
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
    response_model=PromotionGetDto,
    tags=["promotion"],
    summary="Find Promotion by id",
)
async def get_promotion_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["promotion"],
    summary="Create Promotion",
    dependencies=[Depends(require_admin)]
)
async def create_promotion(
    promotion: PromotionCreateDto, 
    db: Session = Depends(get_db)
):
    return create(db, promotion)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["promotion"],
    summary="Update Promotion",
    dependencies=[Depends(require_admin)]
)
async def update_promotion(
    id: UUID, 
    promotion: PromotionUpdateDto, 
    db: Session = Depends(get_db)
):
    return update(db, id, promotion)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["promotion"],
    summary="Delete Promotion",
    dependencies=[Depends(require_admin)]
)
async def delete_promotion(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return delete_by_id(db, id)
