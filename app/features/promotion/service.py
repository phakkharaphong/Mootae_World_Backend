from datetime import datetime
import random
import string
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


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(Promotion).offset(offset).limit(limit).all()
    total = db.query(Promotion).count()
    response = [PromotionGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[PromotionGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(Promotion).filter(Promotion.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="promotion not found")
        promotion_get_dto = PromotionGetDto.model_validate(vars(response))
        return promotion_get_dto


def create(db: Session, promotion: PromotionCreateDto):
    if not promotion:
        raise HTTPException(status_code=400, detail="Invalid promotion data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_promotion = Promotion(
        id=random_string,
        promocode=promotion.promocode,
        promotion_title=promotion.promotion_title,
        start_date=promotion.start_date,
        end_date=promotion.end_date,
        discount=promotion.discount,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=promotion.created_by,
    )

    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    
    created_dto = PromotionGetDto.model_validate(new_promotion)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, promotion: PromotionUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(Promotion).filter(Promotion.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="promotion not found")

    update_data = promotion.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    promotion_dict = {
        "id": response.id,
        "promocode": response.promocode,
        "promotion_title": response.promotion_title,
        "start_date": response.start_date,
        "end_date": response.end_date,
        "discount": response.discount,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=promotion_dict)


def delete_by_id(db: Session, id: str):
    response = db.query(Promotion).filter(Promotion.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="promotion not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
