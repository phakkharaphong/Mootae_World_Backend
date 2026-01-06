from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.router import require_admin
from app.features.order_payment.dto import OrderPaymentCreateDto, OrderPaymentGetDto, OrderPaymentJoinGetDto
from app.features.order_payment.service import create, find_all, find_by_Order_id, find_by_id
from app.utils.response import PaginatedResponse, ResponseModel


router = APIRouter(
    prefix="/order-payment",
    tags=["order-payment"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[OrderPaymentGetDto],
    tags=["order-payment"],
    summary="Find Order Payments",
    dependencies=[Depends(require_admin)],
)
async def get_all_order_payments(
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return find_all(db=db, page=page, limit=limit)


@router.get(
    "/{id}",
    response_model=OrderPaymentGetDto,
    tags=["order-payment"],
    summary="Find Order Payment by id",
)
async def get_order_payment_by_id(
    id: UUID,
    db: Session = Depends(get_db),
):
    return find_by_id(db=db, id=id)


@router.get(
    "/OrderId/{OrderId}",
    response_model=OrderPaymentJoinGetDto,
    tags=["order-payment"],
    summary="Find Order Payment by Order id",
)
async def get_order_payment_by_orderid(
    OrderId: UUID,
    db: Session = Depends(get_db),
):
    return find_by_Order_id(db=db, OrderId=OrderId)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["order-payment"],
    summary="Create Order Payment",
)
async def create_order_payment(
    payment: OrderPaymentCreateDto,
    db: Session = Depends(get_db),
):
    return create(db=db, payment=payment)
