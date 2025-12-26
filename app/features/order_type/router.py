from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.order_type.dto import (
    OrderTypeCreateDto,
    OrderTypeGetDto,
    OrderTypeUpdateDto,
    OrderTypeUpdateDto,
)
from app.features.order_type.service import (
    OrderTypeSortField,
    find_all,
    find_by_id,
    create,
    update,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


router = APIRouter(
    prefix="/order-type",
    tags=["order-type"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[OrderTypeGetDto],
    tags=["order-type"],
    summary="Find Order Type",
)
async def get_all_order_type(
    search: str | None = None,
    sort_by: OrderTypeSortField | None = "created_at",
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
    response_model=OrderTypeGetDto,
    tags=["order-type"],
    summary="Find Order Type by id",
)
async def get_order_type_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["order-type"],
    summary="Create Order Type",
    dependencies=[Depends(require_admin)]
)
async def create_order_type(
    order_type: OrderTypeCreateDto, 
    db: Session = Depends(get_db)
):
    return create(db, order_type)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["order-type"],
    summary="Update Order Type",
    dependencies=[Depends(require_admin)]
)
async def update_order_type(
    id: UUID, 
    order_type: OrderTypeUpdateDto, 
    db: Session = Depends(get_db)
):
    return update(db, id, order_type)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["order-type"],
    summary="Delete Order Type",
    dependencies=[Depends(require_admin)]
)
async def delete_order_type(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return delete_by_id(db, id)
