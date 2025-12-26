from datetime import datetime
import random
import string
from typing import Literal, TypeAlias
from uuid import UUID
from fastapi import HTTPException
import pytz

from app.features.promotion.model import Promotion
from app.features.promotion.dto import (
    PromotionCreateDto,
    PromotionCreateDto,
    PromotionGetDto,
    PromotionUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session

from app.utils.sort import SortOrder

PromotionSortField: TypeAlias = Literal["promotion_title","start_date", "end_date", "is_active" ,"created_at"]


def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: PromotionSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 0,
    limit: int = 100,
    ):

    offset = (page - 1) * limit

    query = db.query(Promotion)


    if search:
        search_term = f"%{search}%"
        query = query.filter(Promotion.promotion_title.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(Promotion, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(Promotion.is_active == is_active)

    data = query.offset(offset).limit(limit).all()

    total = query.count()

    return PaginatedResponse(
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
        response = db.query(Promotion).filter(Promotion.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="promotion not found")
        promotion_get_dto = PromotionGetDto.model_validate(vars(response))
        return promotion_get_dto


def create(
        db: Session, 
        promotion: PromotionCreateDto
    ):
    if not promotion:
        raise HTTPException(status_code=400, detail="Invalid promotion data")

    new_promotion = Promotion(
        promocode=promotion.promocode,
        promotion_title=promotion.promotion_title,
        start_date=promotion.start_date,
        end_date=promotion.end_date,
        discount=promotion.discount,
        is_active=True,
        # created_at=datetime.now(thai_timezone),
        # created_by=promotion.created_by,
    )

    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    
    created_dto = PromotionGetDto.model_validate(new_promotion)
    return ResponseModel(
        status=201, 
        message="Created success", 
        data=created_dto
    )


def update(
        db: Session, 
        id: UUID, 
        promotion: PromotionUpdateDto
    ):

    response = db.query(Promotion).filter(Promotion.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="promotion not found")

    update_data = promotion.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    promotion_dict = {
        "promocode": response.promocode,
        "promotion_title": response.promotion_title,
        "start_date": response.start_date,
        "end_date": response.end_date,
        "discount": response.discount,
        "is_active": response.is_active,
        # "updated_at": response.updated_at,
        # "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200,
        message="Updated success", 
        data=promotion_dict
    )


def delete_by_id(
        db: Session, 
        id: UUID
    ):
    response = db.query(Promotion).filter(Promotion.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="promotion not found")

    db.delete(response)
    db.commit()

    return ResponseModel(
        status=200, 
        message="Deleted success", 
        data=id
    )
