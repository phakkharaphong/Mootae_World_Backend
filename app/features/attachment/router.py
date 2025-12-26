from datetime import datetime
import random
import shutil
import string
from fastapi import APIRouter, Depends, UploadFile, HTTPException
import pytz
from requests import Session

from app.core.database import get_db
from app.features.attachment.dto import AttachmentCreateDto, AttachmentGetDto
from app.features.attachment.model import Attachment
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


@router.post(
        "/uploadfile/",
        tags=["attachment"],
        summary="Uploadfile"
        )
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    try:
        file_location = f"./app/Upload/{file.filename}"

    # Save the file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
       return {"message": f"There was an error uploading the file: {e}"}
    finally:
        if not file:
            raise HTTPException(status_code=400, detail="Invalid attachment data")

        thai_timezone = pytz.timezone("Asia/Bangkok")
        length = 50
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )

        new_attachment = Attachment(
            id=random_string,
            fileName=file.filename,
            content_type=file.content_type,
            fileLocation= file_location,
            fileSize=file.size,
            # mime=attachment.mime,
            created_at=datetime.now(thai_timezone),
            created_by="Admin01",
        )
        db.add(new_attachment)
        db.commit()
        db.refresh(new_attachment)

        created_dto = AttachmentGetDto.model_validate(new_attachment)

        file.file.close()

    return {
        "message": "File uploaded successfully!", 
        "filename": file.filename,
        "file_Size": file.size,
        "file_content_type":file.content_type, 
        "file_headers": file.headers
        }

router.get(
    "/{id}",
    tags=["attachment"],
    summary="Get detail file"
)
async def getDetailFile(id: str):
    print(id)