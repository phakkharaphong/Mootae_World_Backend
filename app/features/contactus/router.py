
from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session
from app.core.database import get_db
from app.utils.response import PaginatedResponse, ResponseModel
from app.features.contactus.service import (
    ContactUsSortField,
    create,
    find_all,
    find_by_id
)
from app.features.contactus.dto import (
    ContactUsCreateDto,
    ContactUsGetDto
)
from app.utils.sort import SortOrder

router = APIRouter(
    prefix="/contactus",
    tags=["contactus"],
)



@router.post(
    "/",
    response_model=ResponseModel,
    tags=["contactus"],
    summary="Create contactus",
)
async def create_category(contactus: ContactUsCreateDto, db: Session = Depends(get_db)):
    return create(db, contactus)


@router.get(
    "/",
    response_model=PaginatedResponse[ContactUsGetDto],
    tags=["contactus"],
    summary="Find contactus",
)
async def get_all_contactus(
    search: str | None = None,
    sort_by: ContactUsSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return find_all(   
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
        )


@router.get(
    "/{id}",
    response_model=ContactUsGetDto,
    tags=["contactus"],
    summary="Find contactus by id",
)
async def get_contactus_by_id(
    id: UUID, 
    db: Session = Depends(get_db)
):
    return find_by_id(db, id)

