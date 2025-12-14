from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.slide_activity.model import SlideActivity
from app.features.slide_activity.dto import (
    SlideActivityCreateDto,
    SlideActivityGetDto,
    SlideActivityUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(SlideActivity).offset(offset).limit(limit).all()
    total = db.query(SlideActivity).count()
    response = [SlideActivityGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[SlideActivityGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(SlideActivity).filter(SlideActivity.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="slide activity not found")
        slide_activity_get_dto = SlideActivityGetDto.model_validate(vars(response))
        return ResponseModel(status=200, message="success", data=slide_activity_get_dto)


def create(db: Session, slide_activity: SlideActivityCreateDto):
    if not slide_activity:
        raise HTTPException(status_code=400, detail="Invalid slide activity data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_slide_activity = SlideActivity(
        id=random_string,
        title=slide_activity.title,
        img_file_name=slide_activity.img_file_name,
        img_path=slide_activity.img_path,
        like=slide_activity.like,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=slide_activity.created_by,
    )

    db.add(new_slide_activity)
    db.commit()
    db.refresh(new_slide_activity)
    
    created_dto = SlideActivityGetDto.model_validate(new_slide_activity)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, slide_activity: SlideActivityUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(SlideActivity).filter(SlideActivity.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="slide activity not found")

    update_data = slide_activity.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    slide_activity_dict = {
        "id": response.id,
        "title": response.title,
        "img_file_name": response.img_file_name,
        "img_path": response.img_path,
        "like": response.like,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, message="Updated success", data=slide_activity_dict
    )


def delete_by_id(db: Session, id: str):
    response = db.query(SlideActivity).filter(SlideActivity.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="slide activity not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
