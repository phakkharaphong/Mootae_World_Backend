from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session

from app.core.database import get_db
from app.features.externalbi.dto import BiOrderStatusDto, BiOrderTypeItem, ExternalBiDto
from app.features.externalbi.service import (
  find_bi_email,
  find_bi_total_type,
  find_bi_total_status
)
from app.utils.response import PaginatedResponse, ResponseBiModel

router = APIRouter(
    prefix="/externalbi",
    tags=["externalbi"],
)



@router.get(
    "/",
    response_model=ResponseBiModel[ExternalBiDto],
    tags=["externalbi"],
    summary="externalbi",
    
)
async def getexternalbi(
    db: Session = Depends(get_db)
):
    return find_bi_email(db)


@router.get(
    "/type",
    response_model=ResponseBiModel[BiOrderTypeItem],
    tags=["externalbi"],
    summary="Count total By Ordertype",
    
)
async def gettype(
    db: Session = Depends(get_db)
):
    return find_bi_total_type(db)


@router.get(
    "/status",
    response_model=ResponseBiModel[BiOrderStatusDto],
    tags=["externalbi"],
    summary="Count total By Status",
    
)
async def gettype(
    db: Session = Depends(get_db)
):
    return find_bi_total_status(db)
