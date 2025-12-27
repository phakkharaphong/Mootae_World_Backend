from typing import Literal, TypeAlias
from uuid import UUID
from sqlalchemy.orm import Session

from app.features.wallpaper.dto import (
    WallpaperCreateDto,
    WallpaperUpdateDto,
)
from app.features.wallpaper.model import Wallpaper
from app.utils.response import PaginatedResponse, Pagination
from app.utils.sort import SortOrder

WallpaperSortField: TypeAlias = Literal["url"]


def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: WallpaperSortField | None = "url",
    sort_order: SortOrder | None = "desc",
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit

    query = db.query(Wallpaper)

    if search:
        search_term = f"%{search}%"
        query = query.filter(Wallpaper.url.ilike(search_term))
    if sort_by:
        sort_column = getattr(Wallpaper, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
        query = query.order_by(sort_column)

    data = query.offset(offset).limit(limit).all()

    total = query.count()

    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: UUID):
    if id:
        response = db.query(Wallpaper).filter(Wallpaper.id == id).first()

        if not response:
            return None

        return response


def create(db: Session, wallpaper: WallpaperCreateDto):
    new_wallpaper = Wallpaper(
        url=wallpaper.url,
        wallpaper_collection_id=wallpaper.wallpaper_collection_id,
    )
    db.add(new_wallpaper)
    db.commit()
    db.refresh(new_wallpaper)
    return new_wallpaper


def update(db: Session, id: UUID, wallpaper: WallpaperUpdateDto):
    existed_wallpaper = db.query(Wallpaper).filter(Wallpaper.id == id).first()
    if existed_wallpaper:
        if wallpaper.url is not None:
            existed_wallpaper.url = wallpaper.url
        if wallpaper.wallpaper_collection_id is not None:
            existed_wallpaper.wallpaper_collection_id = (
                wallpaper.wallpaper_collection_id
            )
        db.commit()
        db.refresh(existed_wallpaper)
        return existed_wallpaper
    return None


def delete(db: Session, id: UUID):
    record = db.query(Wallpaper).filter(Wallpaper.id == id).first()
    if record:
        db.delete(record)
        db.commit()
        return True
    return False
