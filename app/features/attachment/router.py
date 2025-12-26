from datetime import datetime
from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
import pytz
from requests import Session

from app.core.database import get_db
from app.features.attachment.dto import AttachmentCreateDto, AttachmentGetDto
from app.features.attachment.model import Attachment
from app.features.attachment.service import create
from app.utils.response import ResponseModel
from app.core.config import settings

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


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


@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in {"image/png", "image/jpeg"}:
        raise HTTPException(400, "Invalid file type")

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    path = UPLOAD_DIR / filename

    with path.open("wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    new_attachment = Attachment(
        id=str(uuid.uuid4()),
        fileName=file.filename,
        content_type=file.content_type,
        fileLocation=str(path),
        fileSize=path.stat().st_size,
        mime=ext,
        created_at=datetime.now(pytz.timezone("Asia/Bangkok")),
        created_by="System",
    )

    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)

    return {
        "original_name": file.filename,
        "stored_name": filename,
        "content_type": file.content_type,
        "path": str(path),
    }


@router.get("/{id}", tags=["attachment"], summary="Get detail file")
async def get_attachment(id: str, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.id == id).first()
    if not attachment:
        raise HTTPException(404, "Attachment not found")
    attachment_dto = AttachmentGetDto.model_validate(vars(attachment))
    return ResponseModel(status=200, message="Success", data=attachment_dto)
