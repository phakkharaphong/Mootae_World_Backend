from typing import Literal, TypeAlias
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.features.user.error import UserAlreadyExistsError, UserNotFoundError
from app.features.user.model import User
from app.features.user.dto import UserCreateDto, UserUpdateDto
from app.utils.password import hash_password
from app.utils.response import PaginatedResponse, Pagination
from app.utils.sort import SortOrder


UserSortField: TypeAlias = Literal["username", "f_name", "l_name", "created_at"]


def find_all(
    db: Session,
    *,
    search: str | None = None,
    sort_by: UserSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 0,
    limit: int = 100,
):
    offset = (page - 1) * limit

    query = db.query(User)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            User.username.ilike(search_term)
            | User.f_name.ilike(search_term)
            | User.l_name.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(User, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
        query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    data = query.offset(offset).limit(limit).all()

    total = query.count()

    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(
    db: Session,
    id: UUID,
    *,
    search: str | None = None,
    sort_by: UserSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
):
    query = db.query(User).filter(User.id == id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            User.username.ilike(search_term)
            | User.f_name.ilike(search_term)
            | User.l_name.ilike(search_term)
        )
    if sort_by:
        sort_column = getattr(User, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
        query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.first()


def create(db: Session, user: UserCreateDto):
    existed_user = db.query(User).filter(User.username == user.username).first()
    if existed_user:
        raise UserAlreadyExistsError(
            f"User with username '{user.username}' already exists."
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_password,
        f_name=user.f_name,
        l_name=user.l_name,
        phone=user.phone,
        img_profile=user.img_profile,
        address=user.address,
        is_admin=user.is_admin,
        is_active=user.is_active,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


def update(db: Session, id: UUID, user: UserUpdateDto):
    existing_user = db.query(User).filter(User.id == id).first()
    if not existing_user:
        raise UserNotFoundError(f"User with id '{id}' not found.")

    existing_user.f_name = user.f_name
    existing_user.l_name = user.l_name
    existing_user.phone = user.phone
    existing_user.img_profile = user.img_profile
    existing_user.address = user.address
    existing_user.is_admin = user.is_admin
    existing_user.is_active = user.is_active

    db.commit()
    db.refresh(existing_user)


def delete_by_id(db: Session, id: str):
    existing_user = db.query(User).filter(User.id == id).first()
    if not existing_user:
        raise UserNotFoundError(f"User with id '{id}' not found.")

    db.delete(existing_user)
    db.commit()
