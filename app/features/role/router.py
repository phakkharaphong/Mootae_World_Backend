from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.role.dto import RoleCreateDto, RoleGetDto
from app.features.role.service import (
    find_all,
    create,
)
from app.utils.response import PaginatedResponse, ResponseModel


router = APIRouter(
    prefix="/role",
    tags=["role"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[RoleGetDto],
    tags=["role"],
    summary="Find Role",
)
async def get_all_role(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    return find_all(db, page, limit)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["role"],
    summary="Create Role",
)
async def create_role(role: RoleCreateDto, db: Session = Depends(get_db)):
    return create(db, role)
