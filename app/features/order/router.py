from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.order.dto import OrderCreateDto, OrderGetDto, OrderUpdateDto
from app.features.order.service import (
    find_all,
    find_by_email,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[OrderGetDto],
    tags=["order"],
    summary="Find Order",
)
async def get_all_order(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    return find_all(db, page, limit)


@router.get(
    "/by-email/{email}",
    response_model=PaginatedResponse[OrderGetDto],
    tags=["order"],
    summary="Find Order by email",
)
async def get_order_by_email(
    email: str, page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_by_email(db, email, page, limit)


@router.get(
    "/{id}",
    response_model=OrderGetDto,
    tags=["order"],
    summary="Find Order by id",
)
async def get_order_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["order"],
    summary="Create Order",
)
async def create_order(order: OrderCreateDto, db: Session = Depends(get_db)):
    return create(db, order)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["order"],
    summary="Update Order",
)
async def update_order(id: str, order: OrderUpdateDto, db: Session = Depends(get_db)):
    return update_by_id(db, id, order)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["order"],
    summary="Delete Order",
)
async def delete_order(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
