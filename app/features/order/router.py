from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin
from app.features.order.dto import OrderCreateDto, OrderGetDto, OrderUpdateDto
from app.features.order.service import (
    OrderSortField,
    cancel_order_by_id,
    complete_order_by_id,
    find_all,
    find_by_email,
    find_by_id,
    generate_payment_qr,
    create,
    reject_order_by_id,
    update,
    delete_by_id,
    find_by_ordernumber
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
    dependencies=[Depends(require_admin)],
)
async def get_all_order(
    search: str | None = None,
    sort_by: OrderSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return find_all(
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )


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
    db: Session = Depends(get_db),
):
    return find_by_email(
        db=db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        email=email,
        page=page,
        limit=limit,
    )

@router.get(
    "/by-order-number/{order_no}",
    response_model=PaginatedResponse[OrderGetDto],
    tags=["order"],
    summary="Find Order by Order Number",
)
async def get_order_by_order_number(
    order_no: str,
    page: int = 1,
    limit: int = 100,
    search: str | None = None,
    sort_by: OrderSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    db: Session = Depends(get_db),
):
    return find_by_ordernumber(
        db=db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        order_no=order_no,
        page=page,
        limit=limit,
    )


@router.get(
    "/{id}",
    response_model=OrderGetDto,
    tags=["order"],
    summary="Find Order by id",
)
async def get_order_by_id(id: UUID, db: Session = Depends(get_db)):
    return find_by_id(db=db, id=id)


@router.get(
    "/payment/{id}",
    tags=["order"],
    summary="Get PromptPay QR payload for an order",
)
async def get_order_payment_qr(id: UUID, db: Session = Depends(get_db)):
    return generate_payment_qr(db=db, order_id=id)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["order"],
    summary="Create Order",
)
async def create_order(order: OrderCreateDto, db: Session = Depends(get_db)):
    return create(db=db, order=order)


@router.patch(
    "/{id}",
    response_model=ResponseModel,
    tags=["order"],
    summary="Update Order",
    dependencies=[Depends(require_admin)],
)
async def update_order(id: UUID, order: OrderUpdateDto, db: Session = Depends(get_db)):
    return update(db=db, id=id, order=order)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["order"],
    summary="Delete Order",
    dependencies=[Depends(require_admin)],
)
async def delete_order(id: UUID, db: Session = Depends(get_db)):
    return delete_by_id(db, id)

# @router.patch(
#     "/{id}/cancel",
#     response_model=ResponseModel,
#     tags=["order"],
#     summary="Cancel Order",
# )
# async def cancel_order(id: UUID, db: Session = Depends(get_db)):
#     return cancel_order_by_id(db=db, id=id)

@router.patch(
    "/{id}/complete",
    response_model=ResponseModel,
    tags=["order"],
    summary="Complete Order",
    dependencies=[Depends(require_admin)],
)
async def complete_order(id: UUID, db: Session = Depends(get_db)):
    return complete_order_by_id(db=db, id=id)

@router.patch(
    "/{id}/reject",
    response_model=ResponseModel,
    tags=["order"],
    summary="Reject Order",
    dependencies=[Depends(require_admin)],
)
async def reject_order(id: UUID, db: Session = Depends(get_db)):
    return reject_order_by_id(db=db, id=id)