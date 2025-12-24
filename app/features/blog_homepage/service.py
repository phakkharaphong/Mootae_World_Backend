from datetime import datetime
import random
import string
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


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(BlogHomepage).offset(offset).limit(limit).all()
    total = db.query(BlogHomepage).count()
    response = [BlogHomePageGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[BlogHomePageGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(BlogHomepage).filter(BlogHomepage.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="blog not found")
        blog_home_page_dto = BlogHomePageGetDto.model_validate(vars(response))
        return blog_home_page_dto


def create(db: Session, blog_home_page: BlogHomePageCreateDto):
    if not blog_home_page:
        raise HTTPException(status_code=400, detail="Invalid blog data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_blog_home_page = BlogHomepage(
        id=random_string,
        title=blog_home_page.title,
        note=blog_home_page.note,
        img_path=blog_home_page.img_path,
        link=blog_home_page.link,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=blog_home_page.created_by,
    )

    db.add(new_blog_home_page)
    db.commit()
    db.refresh(new_blog_home_page)

    created_dto = BlogHomePageGetDto.model_validate(new_blog_home_page)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, blog_home_page: BlogHomePageUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(BlogHomepage).filter(BlogHomepage.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    update_data = blog_home_page.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    blog_home_page_dict = {
        "id": response.id,
        "title": response.title,
        "note": response.note,
        "img_path": response.img_path,
        "link": response.link,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, message="Updated success", data=blog_home_page_dict
    )


def delete_by_id(db: Session, id: str):
    response = db.query(BlogHomepage).filter(BlogHomepage.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
