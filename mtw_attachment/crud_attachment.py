from fastapi import HTTPException, Header,status

from utils.response import ResponseModel
from . import entites_attachment, schema_attachment
from sqlalchemy.orm import Session
import pytz , random, string
from datetime import datetime
def create(db: Session, attachment: schema_attachment.createAttachment, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    thaiTimezone = pytz.timezone('Asia/Bangkok')
    idLength = 50
    randomString = ''.join(random.choices(string.ascii_letters + string.digits, k=idLength))
    dbAttachment = entites_attachment.mtw_attachment(
        id = randomString,
        fileName = attachment.fileName,
        content_type = attachment.content_type,
        fileLocation = attachment.fileLocation,
        fileSize = attachment.fileSize,
        mime = attachment.mime,
        created_at = datetime.now(thaiTimezone),
        created_by = 'Admin01'
    )

    db.add(dbAttachment)
    db.commit()
    db.refresh(dbAttachment)
    return ResponseModel(
    status=201,
    message="created success",
    data=schema_attachment.mtw_attachment.model_validate(dbAttachment)
    )