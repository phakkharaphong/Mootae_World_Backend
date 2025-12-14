from fastapi import HTTPException

from app.features.location.model import Province, Zone
from app.features.location.dto import ProvinceGetDto, ZoneGetDto
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all_province(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(Province).offset(offset).limit(limit).all()
    total = db.query(Province).count()
    response = [ProvinceGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[ProvinceGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_all_zone(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(Zone).offset(offset).limit(limit).all()
    total = db.query(Zone).count()
    response = [ZoneGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[ZoneGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_province_by_id(db: Session, id: int):
    if id:
        response = db.query(Province).filter(Province.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="province not found")
        province_get_dto = ProvinceGetDto.model_validate(vars(response))
        return ResponseModel(status=200, message="success", data=province_get_dto)
