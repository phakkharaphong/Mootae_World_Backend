from fastapi import APIRouter
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.location.dto import ProvinceGetDto
from app.features.location.service import (
    find_all_province,
    find_all_zone,
    find_province_by_id,
)
from app.utils.response import PaginatedResponse


router = APIRouter(
    prefix="/location",
    tags=["location"],
)


@router.get(
    "/province",
    response_model=PaginatedResponse[ProvinceGetDto],
    tags=["location"],
    summary="Find Province",
)
async def get_all_province(
    page: int = 1, limit: int = 100, db: Session = Depends(get_db)
):
    return find_all_province(db, page, limit)


@router.get(
    "/zone",
    response_model=PaginatedResponse[ProvinceGetDto],
    tags=["location"],
    summary="Find Zone",
)
async def get_all_zone(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    return find_all_zone(db, page, limit)


@router.get(
    "/province/{id}",
    response_model=ProvinceGetDto,
    tags=["location"],
    summary="Find Province by id",
)
async def get_province_by_id(id: int, db: Session = Depends(get_db)):
    return find_province_by_id(db, id)
