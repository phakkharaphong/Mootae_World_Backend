from fastapi import HTTPException

from app.features.attachment.dto import AttachmentCreateDto, AttachmentGetDto
from app.features.attachment.model import Attachment
from app.utils.response import ResponseModel
from sqlalchemy.orm import Session
import pytz, random, string
from datetime import datetime


def create(db: Session, attachment: AttachmentCreateDto):
    if not attachment:
        raise HTTPException(status_code=400, detail="Invalid attachment data")

    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    new_attachment = Attachment(
        id=random_string,
        fileName=attachment.fileName,
        content_type=attachment.content_type,
        fileLocation=attachment.fileLocation,
        fileSize=attachment.fileSize,
        mime=attachment.mime,
        created_at=datetime.now(thai_timezone),
        created_by="Admin01",
    )

    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)

    created_dto = AttachmentGetDto.model_validate(new_attachment)
    return ResponseModel(status=201, message="Created success", data=created_dto)
