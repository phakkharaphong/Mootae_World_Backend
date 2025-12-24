from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.order_type.model import OrderType
from app.features.order_type.dto import (
    OrderTypeCreateDto,
    OrderTypeGetDto,
    OrderTypeUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(OrderType).offset(offset).limit(limit).all()
    total = db.query(OrderType).count()
    response = [OrderTypeGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[OrderTypeGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(OrderType).filter(OrderType.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="order type not found")
        order_type_get_dto = OrderTypeGetDto.model_validate(vars(response))
        return order_type_get_dto


def create(db: Session, order_type: OrderTypeCreateDto):
    if not order_type:
        raise HTTPException(status_code=400, detail="Invalid order type data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_order_type = OrderType(
        id=random_string,
        type_name=order_type.type_name,
        price=order_type.price,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=order_type.created_by,
    )

    db.add(new_order_type)
    db.commit()
    db.refresh(new_order_type)
    
    created_dto = OrderTypeGetDto.model_validate(new_order_type)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, order_type: OrderTypeUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(OrderType).filter(OrderType.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order type not found")

    update_data = order_type.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    order_type_dict = {
        "id": response.id,
        "type_name": response.type_name,
        "price": response.price,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=order_type_dict)


def delete_by_id(db: Session, id: str):
    response = db.query(OrderType).filter(OrderType.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order type not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
