from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.blog.model import Blog
from app.features.blog.dto import BlogCreateDto, BlogGetDto, BlogUpdateDto
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session, joinedload


def find_all(
    db: Session,
    page: int = 0,
    limit: int = 100,
    categories_id: str | None = None,
    keyword: str | None = None,
    is_active: bool | None = None,
):
    offset = (page - 1) * limit
    query = db.query(Blog).options(joinedload(Blog.category))
    if keyword:
        query = query.filter(Blog.title.ilike(f"%{keyword}%"))
    if categories_id:
        query = query.filter(Blog.category_id == categories_id)
    if is_active is not None:
        query = query.filter(Blog.is_active == is_active)
    total = query.count()
    rows = query.offset(offset).limit(limit).all()
    response = [BlogGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[BlogGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(Blog).filter(Blog.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="blog not found")
        response.view += 1
        db.commit()
        db.refresh(response)
        blog_get_dto = BlogGetDto.model_validate(vars(response))
        return blog_get_dto


def create(db: Session, blog: BlogCreateDto):
    if not blog:
        raise HTTPException(status_code=400, detail="Invalid blog data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_blog = Blog(
        id=random_string,
        title=blog.title,
        cover_img=blog.cover_img,
        content=blog.content,
        view=0,
        like=0,
        category_id=blog.category_id,
        is_active=blog.is_active,
        created_at=datetime.now(thai_timezone),
        created_by=blog.created_by,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    created_dto = BlogGetDto.model_validate(new_blog)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, blog: BlogUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(Blog).filter(Blog.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    update_data = blog.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    blog_dict = {
        "id": response.id,
        "title": response.title,
        "cover_img": response.cover_img,
        "content": response.content,
        "view": response.view,
        "like": response.like,
        "category_id": response.category_id,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=blog_dict)


def delete_by_id(db: Session, id: str):
    response = db.query(Blog).filter(Blog.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="blog not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data=id)
