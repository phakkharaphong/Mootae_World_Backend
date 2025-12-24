from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.footer_website.model import FooterWebsite
from app.features.footer_website.dto import (
    FooterWebsiteCreateDto,
    FooterWebsiteGetDto,
    FooterWebsiteUpdateDto,
)
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(FooterWebsite).offset(offset).limit(limit).all()
    total = db.query(FooterWebsite).count()
    response = [FooterWebsiteGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[FooterWebsiteGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(FooterWebsite).filter(FooterWebsite.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="footer website not found")
        footer_website_get_dto = FooterWebsiteGetDto.model_validate(vars(response))
        return footer_website_get_dto


def create(db: Session, footer_website: FooterWebsiteCreateDto):
    if not footer_website:
        raise HTTPException(status_code=400, detail="Invalid footer website data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_footer_website = FooterWebsite(
        id=random_string,
        title=footer_website.title,
        icon_img=footer_website.icon_img,
        link_ref=footer_website.link_ref,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=footer_website.created_by,
    )

    db.add(new_footer_website)
    db.commit()
    db.refresh(new_footer_website)

    created_dto = FooterWebsiteGetDto.model_validate(new_footer_website)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, footer_website: FooterWebsiteUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(FooterWebsite).filter(FooterWebsite.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="footer website not found")

    update_data = footer_website.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    footer_website_dict = {
        "id": response.id,
        "title": response.title,
        "icon_img": response.icon_img,
        "link_ref": response.link_ref,
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
        status=200, message="Updated success", data=footer_website_dict
    )


def delete_by_id(db: Session, id: str):
    response = db.query(FooterWebsite).filter(FooterWebsite.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="footer website not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
