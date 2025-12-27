from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.wallpaper.service import (
    create,
    delete,
    find_all,
    find_by_id,
    update,
)
from app.features.wallpaper.dto import (
    WallpaperCreateDto,
    WallpaperGetDto,
)
from app.utils.response import PaginatedResponse


router = APIRouter(
    prefix="/wallpaper",
    tags=["wallpaper"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[WallpaperGetDto],
    tags=["wallpaper"],
    summary="Find Wallpaper",
)
async def get_all_wallpapers(
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return find_all(
        db,
        page=page,
        limit=limit,
    )


@router.get(
    "/{id}",
    response_model=WallpaperGetDto,
    tags=["wallpaper"],
    summary="Find Wallpaper by id",
)
async def get_wallpaper_by_id(id: UUID, db: Session = Depends(get_db)):
    wallpaper = find_by_id(db, id)
    if not wallpaper:
        return None
    return wallpaper


@router.post(
    "/",
    tags=["wallpaper"],
    summary="Create Wallpaper",
)
async def create_wallpaper(
    wallpaper: WallpaperCreateDto,
    db: Session = Depends(get_db),
):
    return create(db, wallpaper)


@router.put(
    "/{id}",
    tags=["wallpaper"],
    summary="Update Wallpaper by id",
)
async def update_wallpaper(
    id: UUID,
    wallpaper: WallpaperCreateDto,
    db: Session = Depends(get_db),
):
    return update(db, id, wallpaper)


@router.delete(
    "/{id}",
    tags=["wallpaper"],
    summary="Delete Wallpaper by id",
)
async def delete_wallpaper(
    id: UUID,
    db: Session = Depends(get_db),
):
    return delete(db, id)
