from fastapi import APIRouter, Depends
from requests import Session

from app.core.database import get_db
from app.features.attachment.dto import AttachmentCreateDto
from app.features.attachment.service import create
from app.utils.response import ResponseModel


router = APIRouter(
    prefix="/attachment",
    tags=["attachment"],
)


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["attachment"],
    summary="Create Attachment",
)
async def create_attachment(
    attachment: AttachmentCreateDto, db: Session = Depends(get_db)
):
    return create(db, attachment)
