from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy import or_

import random
from typing import Literal, TypeAlias
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.features.order.dto import (
    OrderCreateDto,
    OrderGetDto,
    OrderPromptPayQrDto,
    OrderUpdateDto,
)
from app.features.order.model import Order
from app.features.order_type.model import OrderType
from app.utils.response import PaginatedResponse, Pagination, ResponseModel

from app.utils.sort import SortOrder

day_num_maps = [1, 2, 3, 4, 5, 6, 7]
month_num_maps = [3, 4, 5, 6, 7, 1, 2, 4, 4, 5, 1, 2]
year_num_maps = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5]

luck_type_maps = {
    "Love": [24, 42, 22, 28, 26],
    "Charm": [23],
    "Travel": [27],
    "Trade": [29],
    "Work": [45, 46],
    "Finance": [56, 36, 63],
    "Health": [46, 45, 59, 95],
    "Business": [36, 32, 65, 79],
    "Overall": [15, 39, 92],
}

luck_num_maps = {
    1: [4, 5, 9, 0],
    2: [2, 4, 6, 7, 8, 9, 0],
    3: [2, 4, 5, 6, 9, 0],
    4: [2, 5, 6, 7, 0],
    5: [1, 3, 4, 6, 9, 0],
    6: [2, 3, 4, 5, 0],
    7: [2, 4, 5, 6, 8, 9, 0],
    8: [2, 6, 7, 9, 0],
    9: [1, 2, 3, 4, 5, 6, 7, 8, 0],
}

OrderSortField: TypeAlias = Literal[
    "first_name_customer", "last_name_customer", "email", "payment_status", "created_at"
]


def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: OrderSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit

    query = db.query(Order).options(joinedload(Order.order_type))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Order.first_name_customer.ilike(search_term),
                Order.last_name_customer.ilike(search_term),
                Order.email.ilike(search_term),
            )
        )       
    if sort_by:
        sort_column = getattr(Order, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    data = query.offset(offset).limit(limit).all()

    total = query.count()
    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_email(
    db: Session,
    *,
    search: str | None = None,
    sort_by: OrderSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    email: str,
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit
    query = (
        db.query(Order)
        .options(joinedload(Order.order_type))
        .filter(Order.email == email)
    )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Order.first_name_customer.ilike(search_term),
            Order.last_name_customer.ilike(search_term),
            Order.email.ilike(search_term),
        )
    if sort_by:
        sort_column = getattr(Order, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    data = query.offset(offset).limit(limit).all()

    total = query.count()

    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: UUID):
    if id:
        response = db.query(Order).filter(Order.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="order not found")
        order_get_dto = OrderGetDto.model_validate(vars(response))
        return order_get_dto


def create(db: Session, order: OrderCreateDto):
    day_score = 0
    month_score = 0
    zodiac_score = 0
    title_score = 0
    textlist_day = []
    textlist_month = []
    textlist_zodiac = []
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")

    orderType = db.query(OrderType).filter(OrderType.id == order.order_type_id).first()
    if not orderType:
        raise HTTPException(status_code=404, detail="order type not found")
    
    title_score = random.choice(luck_type_maps.get(orderType.type_name, luck_type_maps["Overall"]))
    textlist_day = luck_num_maps[day_num_maps[order.birth_date_customer_number]]
    textlist_month = luck_num_maps[month_num_maps[order.birth_month_customer_number]]
    textlist_zodiac = luck_num_maps[year_num_maps[order.zodiac_customer_number]]

    lists = textlist_day + textlist_month + textlist_zodiac
    # full_text = " ".join(
    #     map(str, [day_score, month_score, zodiac_score, title_score] + lists)
    # )
    full_text = " ".join(
        map(str, [order.birth_date_customer_number, order.birth_month_customer_number, order.zodiac_customer_number, title_score])
    )

    new_order = Order(
        order_type_id=order.order_type_id,
        first_name_customer=order.first_name_customer,
        last_name_customer=order.last_name_customer,
        email=order.email,
        phone=order.phone,
        full_mootext=full_text,
        total_price=orderType.price,
        wallpaper_url=order.wallpaper_url,
        birth_date_customer_number=order.birth_date_customer_number,
        birth_month_customer_number=order.birth_month_customer_number,
        zodiac_customer_number=order.zodiac_customer_number,
        payment_status="Pending",
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    created_dto = OrderGetDto.model_validate(new_order)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update(db: Session, id: UUID, order: OrderUpdateDto):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)
    order_dict = {
        "order_type_id": response.order_type_id,
        "first_name_customer": response.first_name_customer,
        "last_name_customer": response.last_name_customer,
        "birth_date_customer_number": order.birth_date_customer_number,
        "birth_month_customer_number": order.birth_month_customer_number,
        "zodiac_customer_number": order.zodiac_customer_number,
        "wallpaper_url": order.wallpaper_url,
        "phone": response.phone,
        "email": response.email,
        "total_price": response.total_price,
        "payment_status": response.payment_status,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=order_dict)


def delete_by_id(db: Session, id: UUID):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data=id)

def complete_order_by_id(db: Session, id: UUID):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    response.payment_status = "Completed"

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Order completed successfully", data=id)

def cancel_order_by_id(db: Session, id: UUID):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    response.payment_status = "Cancelled"

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Order cancelled successfully", data=id)

def reject_order_by_id(db: Session, id: UUID):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    response.payment_status = "Rejected"

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Order rejected successfully", data=id)

def generate_payment_qr(db: Session, order_id: UUID):

    if not order_id:
        raise HTTPException(status_code=400, detail="Invalid order id")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    if order.total_price is None:
        raise HTTPException(status_code=400, detail="order total_price is missing")

    promptpay_id = settings.PROMPTPAY_ID
    if not promptpay_id:
        raise HTTPException(status_code=500, detail="PROMPTPAY_ID is not configured")

    amount_decimal = Decimal(str(order.total_price)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    payload = _build_promptpay_payload(promptpay_id=promptpay_id, amount=amount_decimal)

    return OrderPromptPayQrDto(
        order_id=order_id,
        amount=float(amount_decimal),
        promptpay_id=_digits_only(promptpay_id),
        promptpay_payload=payload,
    )


def _tlv(tag: str, value: str) -> str:
    length = f"{len(value):02d}"
    return f"{tag}{length}{value}"


def _digits_only(value: str) -> str:
    return "".join(ch for ch in str(value) if ch.isdigit())


def _promptpay_merchant_account_info(promptpay_id: str) -> str:
    digits = _digits_only(promptpay_id)

    # PromptPay spec (common):
    # - subtag 01: mobile number (E.164-like, TH=66)
    # - subtag 02: citizen/tax id (13 digits)
    # Many Thai bank QR parsers expect mobile in PromptPay format: 0066 + 9 digits
    # (i.e. 13 digits total) rather than plain "66" prefix.
    if len(digits) == 10 and digits.startswith("0"):
        mobile_pp = "0066" + digits[1:]
        id_subtag = _tlv("01", mobile_pp)
    elif len(digits) == 11 and digits.startswith("66"):
        mobile_pp = "0066" + digits[2:]
        id_subtag = _tlv("01", mobile_pp)
    elif len(digits) == 13:
        id_subtag = _tlv("02", digits)
    else:
        raise HTTPException(
            status_code=400,
            detail="PROMPTPAY_ID must be a 10-digit TH mobile (starts with 0) or 13-digit citizen/tax id",
        )

    aid = _tlv("00", "A000000677010111")
    return _tlv("29", aid + id_subtag)


def _crc16_ccitt_false(data: str) -> str:
    # CRC-16/CCITT-FALSE
    # poly=0x1021, init=0xFFFF, xorout=0x0000, refin=false, refout=false
    crc = 0xFFFF
    for byte in data.encode("ascii"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) & 0xFFFF) ^ 0x1021
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def _build_promptpay_payload(*, promptpay_id: str, amount: Decimal) -> str:
    # Mandatory fields
    payload = ""
    payload += _tlv("00", "01")  # Payload Format Indicator
    payload += _tlv("01", "12")  # Point of Initiation Method (dynamic)
    payload += _promptpay_merchant_account_info(promptpay_id)
    payload += _tlv("52", "0000")  # Merchant Category Code
    payload += _tlv("53", "764")  # THB

    # Amount (2 decimals)
    amount_str = f"{amount:.2f}"
    payload += _tlv("54", amount_str)

    payload += _tlv("58", "TH")  # Country Code

    # Optional in EMV, but some bank apps are strict and fail to parse without them.
    merchant_name = (getattr(settings, "PROMPTPAY_MERCHANT_NAME", None) or "").strip()
    merchant_city = (getattr(settings, "PROMPTPAY_MERCHANT_CITY", None) or "").strip()
    if merchant_name:
        payload += _tlv("59", merchant_name[:25])
    if merchant_city:
        payload += _tlv("60", merchant_city[:15])

    # CRC
    payload_for_crc = payload + "6304"
    payload += _tlv("63", _crc16_ccitt_false(payload_for_crc))
    return payload
