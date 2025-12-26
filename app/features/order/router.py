from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.order.dto import OrderCreateDto, OrderGetDto, OrderUpdateDto
from app.features.order.service import (
    OrderSortField,
    find_all,
    find_by_email,
    find_by_id,
    create,
    update,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel
from app.utils.sort import SortOrder


router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[OrderGetDto],
    tags=["order"],
    summary="Find Order",
    dependencies=[Depends(require_admin)]
)
async def get_all_order(
    search: str | None = None,
    sort_by: OrderSortField | None = "created_at",
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
        limit=limit,)


@router.get(
    "/by-email/{email}",
    response_model=PaginatedResponse[OrderGetDto],
    tags=["order"],
    summary="Find Order by email",
)
async def get_order_by_email(
    email: str, 
    page: int = 1, 
    limit: int = 100, 
    search: str | None = None,
    sort_by: OrderSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    return find_by_email(db=db, search=search,sort_by=sort_by, sort_order=sort_order, is_active=is_active, email=email, page=page, limit=limit)


@router.get(
    "/{id}",
    response_model=OrderGetDto,
    tags=["order"],
    summary="Find Order by id",
)
async def get_order_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db=db, id=id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["order"],
    summary="Create Order",
)
async def create_order(
    order: OrderCreateDto, 
    db: Session = Depends(get_db)
):
    return create(db=db, order=order)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["order"],
    summary="Update Order",
    dependencies=[Depends(require_admin)]
)
async def update_order(
    id: UUID, 
    order: OrderUpdateDto, 
    db: Session = Depends(get_db)
):
    return update(db=db, id=id, order=order)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["order"],
    summary="Delete Order",
    dependencies=[Depends(require_admin)]
)
async def delete_order(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return delete_by_id(db, id)
