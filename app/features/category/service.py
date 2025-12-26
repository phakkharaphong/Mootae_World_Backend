from datetime import datetime
from uuid import UUID
from typing import Literal, TypeAlias
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

from app.utils.sort import SortOrder

CategorySortField: TypeAlias = Literal["name","created_at"]

def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: CategorySortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 0,
    limit: int = 100,
    ):


    offset = (page - 1) * limit

    query = db.query(Category)

    if search:
        search_term = f"%{search}%"
        query = query.filter(Category.name.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(Category, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(Category.is_active == is_active)

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
        response = db.query(Category).filter(Category.id == id).first()

        if not response:
            raise HTTPException(status_code=404, detail="category not found")
        
        category_get_dto = CategoryGetDto.model_validate(vars(response))
        return category_get_dto


def create(db: Session, category: CategoryCreateDto):
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category data")

    new_category = Category(
        name=category.name,
        is_active=category.is_active,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    created_dto = CategoryGetDto.model_validate(new_category)
   
    return ResponseModel(
        status=201, 
        message="Created success", 
        data=created_dto
    )


def update(db: Session, id: UUID, category: CategoryUpdateDto):
    response = db.query(Category).filter(Category.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    update_data = category.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(response, key, value)

    blog_dict = {
        "id": response.id,
        "title": response.name,
        "is_active": response.is_active,
    }


    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, 
        message="Updated success", 
        data=blog_dict
    )


def delete(db: Session, id: UUID):
    response = db.query(Category).filter(Category.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="category not found")

    db.delete(response)
    db.commit()

    return ResponseModel(
        status=200, 
        message="Deleted success", 
        data=id
    )
