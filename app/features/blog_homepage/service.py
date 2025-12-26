from datetime import datetime
import random
import string
from typing import Literal, TypeAlias
from uuid import UUID
from fastapi import HTTPException
import pytz

from app.features.blog_homepage.model import BlogHomepage
from app.features.blog_homepage.dto import (
    BlogHomePageCreateDto,
    BlogHomePageGetDto,
    BlogHomePageUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session

from app.utils.sort import SortOrder

BlogHomepageSortField: TypeAlias = Literal["title","created_at"]

def find_all(
     db: Session,
    *,
    search: str | None = None,
    sort_by: BlogHomepageSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit

    query = db.query(BlogHomepage)
    if search:
        search_term = f"%{search}%"
        query = query.filter(BlogHomepage.title.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(BlogHomepage, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(BlogHomepage.is_active == is_active)

    data = query.offset(offset).limit(limit).all()

    total = query.count()

    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(
        db: Session, 
        id: str
    ):

    if id:
        response = db.query(BlogHomepage).filter(BlogHomepage.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="blog not found")
        blog_home_page_dto = BlogHomePageGetDto.model_validate(vars(response))
        return blog_home_page_dto


def create(
        db: Session, 
        blog_home_page: BlogHomePageCreateDto
    ):

    if not blog_home_page:
        raise HTTPException(
            status_code=400, 
            detail="Invalid blog data"
        )
    new_blog_home_page = BlogHomepage(
        title=blog_home_page.title,
        note=blog_home_page.note,
        img_path=blog_home_page.img_path,
        link=blog_home_page.link,
        is_active=True,
    )

    db.add(new_blog_home_page)
    db.commit()
    db.refresh(new_blog_home_page)

    created_dto = BlogHomePageGetDto.model_validate(new_blog_home_page)
    return ResponseModel(
        status=201, 
        message="Created success", 
        data=created_dto
    )


def update(
        db: Session, 
        id: UUID, 
        blog_home_page: BlogHomePageUpdateDto
    ):

    response = db.query(BlogHomepage).filter(BlogHomepage.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    update_data = blog_home_page.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(response, key, value)

    blog_home_page_dict = {
        "title": response.title,
        "note": response.note,
        "img_path": response.img_path,
        "link": response.link,
        "is_active": response.is_active,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, 
        message="Updated success", 
        data=blog_home_page_dict
    )


def delete_by_id(
        db: Session, 
        id: UUID
    ):
    response = db.query(BlogHomepage).filter(BlogHomepage.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    db.delete(response)
    db.commit()

    return ResponseModel(
        status=200, 
        message="Deleted success", 
        data=id
    )
