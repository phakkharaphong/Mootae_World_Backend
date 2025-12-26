from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.auth.router import require_admin, require_auth
from app.features.user.dto import UserCreateDto, UserGetDto, UserUpdateDto
from app.features.user.error import UserAlreadyExistsError, UserNotFoundError
from app.features.user.service import (
    UserSortField,
    find_all,
    find_by_id,
    create,
    delete_by_id,
    update,
)
from app.utils.response import PaginatedResponse
from app.utils.sort import SortOrder


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[UserGetDto],
    tags=["user"],
    summary="Find User",
    dependencies=[Depends(require_admin)]
)
async def get_all_user(
    search: str | None = None,
    sort_by: UserSortField | None = "created_at",
    sort_order: SortOrder | None = "desc",
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return find_all(
        db,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        is_active=is_active,
        page=page,
        limit=limit,
    )


@router.get(
    "/{id}",
    response_model=UserGetDto,
    tags=["user"],
    summary="Find User by id",
)
async def get_user_by_id(id: UUID, db: Session = Depends(get_db)):
    user = find_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post(
    "/",
    tags=["user"],
    summary="Create User",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreateDto, db: Session = Depends(get_db)):
    try:
        create(db, user)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )


@router.put(
    "/{id}",
    tags=["user"],
    summary="Update User",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user(id: str, user: UserUpdateDto, db: Session = Depends(get_db)):
    try:
        update(db, id, user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.delete(
    "/{id}",
    tags=["user"],
    summary="Delete User",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def delete_user(id: str, db: Session = Depends(get_db)):
    try:
        delete_by_id(db, id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
