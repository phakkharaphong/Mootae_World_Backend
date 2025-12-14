from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.order_type.dto import (
    OrderTypeCreateDto,
    OrderTypeGetDto,
    OrderTypeUpdateDto,
    OrderTypeUpdateDto,
)
from app.features.order_type.service import (
    find_all,
    find_by_id,
    create,
    update_by_id,
    delete_by_id,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


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
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=OrderTypeGetDto,
    tags=["order-type"],
    summary="Find Order Type by id",
)
async def get_order_type_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["order-type"],
    summary="Create Order Type",
)
async def create_order_type(
    order_type: OrderTypeCreateDto, db: Session = Depends(get_db)
):
    return create(db, order_type)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["order-type"],
    summary="Update Order Type",
)
async def update_order_type(
    id: str, order_type: OrderTypeUpdateDto, db: Session = Depends(get_db)
):
    return update_by_id(db, id, order_type)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["order-type"],
    summary="Delete Order Type",
)
async def delete_order_type(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
