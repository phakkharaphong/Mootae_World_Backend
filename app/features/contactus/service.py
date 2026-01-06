from datetime import datetime, timezone
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
from app.features.contactus.dto import ContactUsCreateDto, ContactUsGetDto
from app.features.contactus.model import ContactUs
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session

from app.utils.sort import SortOrder

ContactUsSortField: TypeAlias = Literal["name","created_at"]

def create(db: Session, contactus: ContactUsCreateDto):
    if not contactus:
        raise HTTPException(status_code=400, detail="Invalid Contact Us data")

    new_contactus = ContactUs(
        name=contactus.name,
        email= contactus.email,
        phone = contactus.phone,
        message = contactus.message,
        created_at = datetime.now(timezone.utc),
        created_by = contactus.email
    )

    db.add(new_contactus)
    db.commit()
    db.refresh(new_contactus)

    created_dto = CategoryGetDto.model_validate(new_contactus)
   
    return ResponseModel(
        status=201, 
        message="Created success", 
        data=created_dto
    )



def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: ContactUsSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    page: int = 0,
    limit: int = 100,
    ):


    offset = (page - 1) * limit

    query = db.query(ContactUs)

    if search:
        search_term = f"%{search}%"
        query = query.filter(ContactUs.name.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(ContactUs, sort_by)
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
        response = db.query(ContactUs).filter(ContactUs.id == id).first()

        if not response:
            raise HTTPException(status_code=404, detail="ContactUs not found")
        
        category_get_dto = ContactUsGetDto.model_validate(vars(response))
        return category_get_dto


