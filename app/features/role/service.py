from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.role.model import Role
from app.features.role.dto import RoleCreateDto, RoleGetDto
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = db.query(Role).offset(offset).limit(limit).all()
    total = db.query(Role).count()
    response = [RoleGetDto.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[RoleGetDto](
        message="success",
        data=response,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def create(db: Session, role: RoleCreateDto):
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_role = Role(
        id=random_string,
        role_name=role.role_name,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=role.created_by,
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    created_dto = RoleGetDto.model_validate(new_role)
    return ResponseModel(status=201, message="Created success", data=created_dto)
