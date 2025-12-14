from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.order.model import Order
from app.features.order.dto import OrderCreateDto, OrderGetDto, OrderUpdateDto
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session, joinedload


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(Order)
        .options(joinedload(Order.order_type))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(Order).count()
    orders = [OrderGetDto.model_validate(r) for r in rows]
    return PaginatedResponse[OrderGetDto](
        message="success",
        data=orders,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_email(db: Session, email: str, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(Order)
        .options(joinedload(Order.order_type))
        .filter(Order.email == email)
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(Order).count()
    orders = [OrderGetDto.model_validate(r) for r in rows]
    return PaginatedResponse[OrderGetDto](
        message="success",
        data=orders,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(Order).filter(Order.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="order not found")
        order_get_dto = OrderGetDto.model_validate(vars(response))
        return ResponseModel(status=200, message="success", data=order_get_dto)


def create(db: Session, order: OrderCreateDto):
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_order = Order(
        id=random_string,
        order_type_id=order.order_type_id,
        emphasize_particular=order.emphasize_particular,
        supplement=order.supplement,
        supplement_other=order.supplement_other,
        birth_date_idol=order.birth_date_idol,
        services_zodiac=order.services_zodiac,
        services_auspicious=order.services_auspicious,
        first_name_customer=order.first_name_customer,
        last_name_customer=order.last_name_customer,
        birth_date_customer=order.birth_date_customer,
        birth_time_customer=order.birth_time_customer,
        gender=order.gender,
        lgbt_description=order.lgbt_description,
        congenital_disease=order.congenital_disease,
        phone=order.phone,
        email=order.email,
        note=order.note,
        newsletter=order.newsletter,
        read_accept_pdpa=order.read_accept_pdpa,
        promotion_id=order.promotion_id,
        total_price=order.total_price,
        payment_status=order.payment_status,
        send_wallpaper_status=order.send_wallpaper_status,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=order.created_by,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    created_dto = OrderGetDto.model_validate(new_order)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, order: OrderUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    order_dict = {
        "id": response.id,
        "order_type_id": response.order_type_id,
        "emphasize_particular": response.emphasize_particular,
        "supplement": response.supplement,
        "supplement_other": response.supplement_other,
        "birth_date_idol": response.birth_date_idol,
        "services_zodiac": response.services_zodiac,
        "services_auspicious": response.services_auspicious,
        "first_name_customer": response.first_name_customer,
        "last_name_customer": response.last_name_customer,
        "birth_date_customer": response.birth_date_customer,
        "birth_time_customer": response.birth_time_customer,
        "gender": response.gender,
        "lgbt_description": response.lgbt_description,
        "congenital_disease": response.congenital_disease,
        "phone": response.phone,
        "email": response.email,
        "note": response.note,
        "newsletter": response.newsletter,
        "read_accept_pdpa": response.read_accept_pdpa,
        "promotion_id": response.promotion_id,
        "total_price": response.total_price,
        "payment_status": response.payment_status,
        "send_wallpaper_status": response.send_wallpaper_status,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=order_dict)


def delete_by_id(db: Session, id: str):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
