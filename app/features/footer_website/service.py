from datetime import datetime
import random
import string
from typing import Literal, TypeAlias
from fastapi import HTTPException
import pytz
from uuid import UUID
from app.features.footer_website.model import FooterWebsite
from app.features.footer_website.dto import (
    FooterWebsiteCreateDto,
    FooterWebsiteGetDto,
    FooterWebsiteUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session

from app.utils.sort import SortOrder

FooterSortField: TypeAlias = Literal["title","created_at"]

def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: FooterSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 0,
    limit: int = 100,
):


    offset = (page - 1) * limit
    query = db.query(FooterWebsite)

    if search:
        search_term = f"%{search}%"
        query = query.filter(FooterWebsite.name.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(FooterWebsite, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(FooterWebsite.is_active == is_active)

    data = query.offset(offset).limit(limit).all()
    query = db.query(FooterWebsite)
    total = query.count()
    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(
        db: Session, 
        id: UUID
    ):
    if id:
        response = db.query(FooterWebsite).filter(FooterWebsite.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="footer website not found")
        
        footer_website_get_dto = FooterWebsiteGetDto.model_validate(vars(response))
        
        return footer_website_get_dto


def create(
        db: Session, 
        footer_website: FooterWebsiteCreateDto
    ):
    if not footer_website:
        raise HTTPException(status_code=400, detail="Invalid footer website data")


    new_footer_website = FooterWebsite(
        title=footer_website.title,
        icon_img=footer_website.icon_img,
        link_ref=footer_website.link_ref,
        is_active=True,
    )

    db.add(new_footer_website)
    db.commit()
    db.refresh(new_footer_website)

    created_dto = FooterWebsiteGetDto.model_validate(new_footer_website)

    return ResponseModel(
        status=201, 
        message="Created success", 
        data=created_dto
    )


def update(
        db: Session, 
        id: UUID, 
        footer_website: FooterWebsiteUpdateDto
    ):

    response = db.query(FooterWebsite).filter(FooterWebsite.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="footer website not found")

    update_data = footer_website.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(response, key, value)

    footer_website_dict = {
        "id": response.id,
        "title": response.title,
        "icon_img": response.icon_img,
        "link_ref": response.link_ref,
        "is_active": response.is_active,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, 
        message="Updated success", 
        data=footer_website_dict
    )


def delete(
        db: Session, 
        id: UUID
    ):
    response = db.query(FooterWebsite).filter(FooterWebsite.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="footer website not found")

    db.delete(response)
    db.commit()

    return ResponseModel(
        status=200, 
        message="Deleted success",
        data=id
    )
