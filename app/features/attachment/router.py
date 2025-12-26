from pathlib import Path
import shutil
import uuid
from fastapi import APIRouter, File, Request, UploadFile, HTTPException
from app.core.config import settings

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter(
    prefix="/attachment",
    tags=["attachment"],
)


@router.post("/upload", status_code=201)
async def upload_file(request: Request, file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg"}:
        raise HTTPException(400, "Invalid file type")

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    path = UPLOAD_DIR / filename

    with path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    file_url = f"{request.base_url}uploads/{filename}"

    return {
        "filename": filename,
        "url": file_url,
    }
