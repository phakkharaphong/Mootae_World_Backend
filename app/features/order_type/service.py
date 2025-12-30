from datetime import datetime
import random
import string
from typing import Literal, TypeAlias
from uuid import UUID
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

from app.utils.sort import SortOrder

OrderTypeSortField: TypeAlias = Literal["type_name","is_active" ,"created_at"]

def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: OrderTypeSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit

    query = db.query(OrderType)

    if search:
        search_term = f"%{search}%"
        query = query.filter(OrderType.type_name.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(OrderType, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(OrderType.is_active == is_active)

    data = query.offset(offset).limit(limit).all()

    total = query.count()
    return PaginatedResponse[OrderTypeGetDto](
        message="success",
        data=data,
        pagination=Pagination(
            page=page, 
            limit=limit, 
            total=total
        ),
    )


def find_by_id(
        db: Session, 
        id: UUID
):
    if id:
        response = db.query(OrderType).filter(OrderType.id == id).first()
        if not response:
            raise HTTPException(
                status_code=404, 
                detail="order type not found"
            )
        order_type_get_dto = OrderTypeGetDto.model_validate(vars(response))
        return order_type_get_dto


def create(
        db: Session, 
        order_type: OrderTypeCreateDto
    ):
    if not order_type:
        raise HTTPException(
            status_code=400, 
            detail="Invalid order type data"
        )

    new_order_type = OrderType(
        type_name=order_type.type_name,
        price=order_type.price,
        key=order_type.key,
        is_active=True,
    )

    db.add(new_order_type)
    db.commit()
    db.refresh(new_order_type)
    
    created_dto = OrderTypeGetDto.model_validate(new_order_type)
    return ResponseModel(
        status=201,
        message="Created success", 
        data=created_dto
    )


def update(
        db: Session, 
        id: UUID, 
        order_type: OrderTypeUpdateDto
):
    response = db.query(OrderType).filter(OrderType.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order type not found")

    update_data = order_type.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    order_type_dict = {
        "type_name": response.type_name,
        "price": response.price,
        "is_active": response.is_active,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, 
        message="Updated success", 
        data=order_type_dict
    )


def delete_by_id(
        db: Session, 
        id: UUID
    ):
    response = db.query(OrderType).filter(OrderType.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order type not found")

    db.delete(response)
    db.commit()

    return ResponseModel(
        status=200, 
        message="Deleted success", 
        data=id
    )
