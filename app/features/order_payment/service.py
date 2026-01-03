from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.order.model import Order
from app.features.order_payment.dto import OrderPaymentCreateDto, OrderPaymentGetDto
from app.features.order_payment.model import OrderPayment
from app.utils.response import PaginatedResponse, Pagination, ResponseModel


def _decimal_to_float(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _to_get_dto(payment: OrderPayment) -> OrderPaymentGetDto:
    return OrderPaymentGetDto(
        id=payment.id,
        order_id=payment.order_id,
        amount=_decimal_to_float(payment.amount),
        slip_url=payment.slip_url,
        payment_date=payment.payment_date.isoformat() if payment.payment_date else None,
        status=payment.status,
        admin_note=payment.admin_note,
        created_at=payment.created_at,
    )


def find_all(db: Session, page: int = 0, limit: int = 100):
    safe_page = page if page and page > 0 else 1
    safe_limit = limit if limit and limit > 0 else 100
    offset = (safe_page - 1) * safe_limit

    query = db.query(OrderPayment)
    data = query.offset(offset).limit(safe_limit).all()
    total = query.count()

    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=safe_page, limit=safe_limit, total=total),
    )


def find_by_id(db: Session, id: UUID):
    if not id:
        raise HTTPException(status_code=400, detail="Invalid payment id")

    payment = db.query(OrderPayment).filter(OrderPayment.id == id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="payment not found")

    return _to_get_dto(payment)


def create(db: Session, payment: OrderPaymentCreateDto):
    if not payment:
        raise HTTPException(status_code=400, detail="Invalid payment data")

    new_payment = OrderPayment(
        order_id=payment.order_id,
        amount=payment.amount,
        slip_url=payment.slip_url,
        status="Pending",
        payment_date=datetime.now(timezone.utc),
    )

    db.add(new_payment)

    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if order:
        order.payment_status = "Verifying"
        db.add(order)

    db.commit()
    db.refresh(new_payment)

    return ResponseModel(
        status=201,
        message="Created success",
        data=_to_get_dto(new_payment),
    )
