from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.slide_news.model import SlideNew
from app.features.slide_news.dto import (
    SlideNewCreateDto,
    SlideNewGetDto,
    SlideNewUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(SlideNew).offset(offset).limit(limit).all()
    total = db.query(SlideNew).count()
    response = [SlideNewGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[SlideNewGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(SlideNew).filter(SlideNew.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="slide activity not found")
        slide_activity_get_dto = SlideNewGetDto.model_validate(vars(response))
        return ResponseModel(status=200, message="success", data=slide_activity_get_dto)


def create(db: Session, slide_news: SlideNewCreateDto):
    if not slide_news:
        raise HTTPException(status_code=400, detail="Invalid slide news data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_slide_news = SlideNew(
        id=random_string,
        title=slide_news.title,
        link_ref=slide_news.link_ref,
        img_path=slide_news.img_path,
        slide_number=slide_news.slide_number,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=slide_news.created_by,
    )

    db.add(new_slide_news)
    db.commit()
    db.refresh(new_slide_news)

    created_dto = SlideNewGetDto.model_validate(new_slide_news)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, slide_news: SlideNewUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(SlideNew).filter(SlideNew.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="slide news not found")

    update_data = slide_news.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    slide_news_dict = {
        "id": response.id,
        "title": response.title,
        "link_ref": response.link_ref,
        "img_path": response.img_path,
        "slide_number": response.slide_number,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=slide_news_dict)


def delete_by_id(db: Session, id: str):
    response = db.query(SlideNew).filter(SlideNew.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="slide activity not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
