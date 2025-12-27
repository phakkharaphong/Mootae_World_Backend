from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.features.wallpaper_collection.service import (
    create,
    delete,
    find_all,
    find_by_id,
    update,
)
from app.features.wallpaper_collection.dto import (
    WallpaperCollectionCreateDto,
    WallpaperCollectionGetDto,
)
from app.utils.response import PaginatedResponse


router = APIRouter(
    prefix="/wallpaper-collection",
    tags=["wallpaper-collection"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[WallpaperCollectionGetDto],
    tags=["wallpaper-collection"],
    summary="Find Wallpaper Collection",
)
async def get_all_wallpaper_collections(
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
    response_model=WallpaperCollectionGetDto,
    tags=["wallpaper-collection"],
    summary="Find Wallpaper Collection by id",
)
async def get_wallpaper_collection_by_id(id: UUID, db: Session = Depends(get_db)):
    wallpaper_collection = find_by_id(db, id)
    if not wallpaper_collection:
        return None
    return wallpaper_collection


@router.post(
    "/",
    tags=["wallpaper-collection"],
    summary="Create Wallpaper Collection",
)
async def create_wallpaper_collection(
    wallpaperCollection: WallpaperCollectionCreateDto,
    db: Session = Depends(get_db),
):
    return create(db, wallpaperCollection)


@router.put(
    "/{id}",
    tags=["wallpaper-collection"],
    summary="Update Wallpaper Collection by id",
)
async def update_wallpaper_collection(
    id: UUID,
    wallpaperCollection: WallpaperCollectionCreateDto,
    db: Session = Depends(get_db),
):
    return update(db, id, wallpaperCollection)


@router.delete(
    "/{id}",
    tags=["wallpaper-collection"],
    summary="Delete Wallpaper Collection by id",
)
async def delete_wallpaper_collection(
    id: UUID,
    db: Session = Depends(get_db),
):
    return delete(db, id)
