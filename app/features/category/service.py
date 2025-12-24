from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.category.model import Category
from app.features.category.dto import (
    CategoryCreateDto,
    CategoryGetDto,
    CategoryUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(Category).offset(offset).limit(limit).all()
    total = db.query(Category).count()
    response = [CategoryGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[CategoryGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(Category).filter(Category.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="category not found")
        category_get_dto = CategoryGetDto.model_validate(vars(response))
        return category_get_dto


def create(db: Session, category: CategoryCreateDto):
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_category = Category(
        id=random_string,
        name=category.name,
        is_active=category.is_active,
        created_at=datetime.now(thai_timezone),
        created_by=category.created_by,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    created_dto = CategoryGetDto.model_validate(new_category)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, category: CategoryUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(Category).filter(Category.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="category not found")

    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    category_dict = {
        "id": response.id,
        "name": response.name,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=category_dict)


def delete_by_id(db: Session, id: str):
    print(id)
    response = db.query(Category).filter(Category.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="category not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data=id)
