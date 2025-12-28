from pathlib import Path
import shutil
import uuid
from io import BytesIO

from fastapi import APIRouter, File, Request, UploadFile, HTTPException

from app.core.config import settings

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_WALLPAPER_DIR = Path(settings.UPLOAD_WALLPAPER_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_WALLPAPER_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter(
    prefix="/attachment",
    tags=["attachment"],
)


def _watermark_bytes(image_bytes: bytes, text: str, ext: str) -> bytes:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as e:
        raise HTTPException(500, "Watermark dependency missing (Pillow)") from e

    fmt = "PNG" if ext.lower() == ".png" else "JPEG"

    with Image.open(BytesIO(image_bytes)) as img:
        base = img.convert("RGBA")
        overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))

        w, h = base.size
        diagonal = (w * w + h * h) ** 0.5

        # Big diagonal watermark across the center.
        angle = -30
        target_width = diagonal * 0.75

        # Start big and adjust down until it fits the target width.
        font_size = max(32, int(min(w, h) * 0.22))

        candidate_font_paths: list[str] = []
        candidate_font_paths.append("app/assets/fonts/Ubuntu-Regular.ttf")

        def load_truetype(size: int):
            for p in candidate_font_paths:
                try:
                    if p and Path(p).exists():
                        return ImageFont.truetype(str(p), size)
                except Exception:
                    continue
            return None

        font = load_truetype(font_size)
        truetype_available = font is not None
        if not truetype_available:
            font = ImageFont.load_default()

        def measure(
            current_font: ImageFont.ImageFont,
        ) -> tuple[tuple[int, int, int, int], int, int]:
            m = ImageDraw.Draw(overlay)
            bbox = m.textbbox((0, 0), text, font=current_font)
            return bbox, bbox[2] - bbox[0], bbox[3] - bbox[1]

        bbox, text_w, text_h = measure(font)
        if truetype_available:
            for _ in range(12):
                if text_w <= target_width:
                    break
                font_size = max(12, int(font_size * 0.9))
                font = load_truetype(font_size) or font
                bbox, text_w, text_h = measure(font)

        pad = max(20, int(min(w, h) * 0.03))
        text_layer = Image.new(
            "RGBA", (text_w + pad * 2, text_h + pad * 2), (255, 255, 255, 0)
        )
        d = ImageDraw.Draw(text_layer)

        # `textbbox()` can return negative left/top values for some fonts.
        # Shift by -bbox[0]/-bbox[1] so glyph ascenders/descenders don't get clipped.
        x0 = pad - bbox[0]
        y0 = pad - bbox[1]

        # Soft shadow + semi-transparent fill.
        shadow = (0, 0, 0, 80)
        fill = (255, 255, 255, 110)
        d.text((x0 + 3, y0 + 3), text, font=font, fill=shadow)
        d.text((x0, y0), text, font=font, fill=fill)

        rotated = text_layer.rotate(angle, expand=True, resample=Image.BICUBIC)
        rx, ry = rotated.size
        pos = ((w - rx) // 2, (h - ry) // 2)
        overlay.paste(rotated, pos, rotated)

        out = Image.alpha_composite(base, overlay)
        if fmt == "JPEG":
            out = out.convert("RGB")

        buf = BytesIO()
        if fmt == "JPEG":
            out.save(buf, format=fmt, quality=90, optimize=True)
        else:
            out.save(buf, format=fmt, optimize=True)
        return buf.getvalue()


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


@router.post("/upload/wallpaper", status_code=201)
async def upload_wallpaper(request: Request, file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg"}:
        raise HTTPException(400, "Invalid file type")

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"

    raw = await file.read()

    original_path = UPLOAD_WALLPAPER_DIR / filename
    with original_path.open("wb") as f:
        f.write(raw)

    watermarked = _watermark_bytes(raw, text="MUTEVERSE", ext=ext)
    public_path = UPLOAD_DIR / filename
    with public_path.open("wb") as f:
        f.write(watermarked)

    file_url = f"{request.base_url}uploads/{filename}"

    return {
        "filename": filename,
        "url": file_url,
    }
