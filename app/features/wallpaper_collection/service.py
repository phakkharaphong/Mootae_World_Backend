from typing import Literal, TypeAlias
from uuid import UUID
from sqlalchemy.orm import Session

from app.features.wallpaper_collection.dto import (
    WallpaperCollectionCreateDto,
    WallpaperCollectionUpdateDto,
)
from app.features.wallpaper_collection.model import WallpaperCollection
from app.utils.response import PaginatedResponse, Pagination
from app.utils.sort import SortOrder

WallpaperCollectionSortField: TypeAlias = Literal["name"]


def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: WallpaperCollectionSortField | None = "name",
    sort_order: SortOrder | None = "desc",
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit

    query = db.query(WallpaperCollection)

    if search:
        search_term = f"%{search}%"
        query = query.filter(WallpaperCollection.name.ilike(search_term))
    if sort_by:
        sort_column = getattr(WallpaperCollection, sort_by)
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
        response = (
            db.query(WallpaperCollection).filter(WallpaperCollection.id == id).first()
        )

        if not response:
            return None

        return response


def create(db: Session, collection: WallpaperCollectionCreateDto):
    new_collection = WallpaperCollection(name=collection.name)
    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)
    return new_collection


def update(db: Session, id: UUID, collection: WallpaperCollectionUpdateDto):
    existed_collection = (
        db.query(WallpaperCollection).filter(WallpaperCollection.id == id).first()
    )
    if existed_collection:
        existed_collection.name = collection.name
        db.commit()
        db.refresh(existed_collection)
        return existed_collection
    return None


def delete(db: Session, id: UUID):
    collection = (
        db.query(WallpaperCollection).filter(WallpaperCollection.id == id).first()
    )
    if collection:
        db.delete(collection)
        db.commit()
        return True
    return False
