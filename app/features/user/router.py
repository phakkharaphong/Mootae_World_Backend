from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.features.user.dto import LoginDto, TokenDto, UserCreateDto, UserGetDto
from app.features.user.service import (
    create_access_token,
    find_all,
    find_by_id,
    create,
    delete_by_id,
    get_username,
)
from app.utils.response import PaginatedResponse, ResponseDeleteModel, ResponseModel


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[UserGetDto],
    tags=["user"],
    summary="Find User",
)
async def get_all_user(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    return find_all(db, page, limit)


@router.get(
    "/{id}",
    response_model=UserGetDto,
    tags=["user"],
    summary="Find User by id",
)
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
    return find_by_id(db, id)


# @router.get(
#     "/me",
#     response_model=UserGetDto,
#     tags=["user"],
#     summary="Get current user",
# )
# async def get_current_user(current_user: UserGetDto = Depends(get_username)):
#     return current_user


@router.post(
    "/token",
    response_model=TokenDto,
    tags=["user"],
    summary="Create Token",
)
async def login_for_access_token(login: LoginDto, db: Session = Depends(get_db)):
    user = get_username(db, login.username, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return TokenDto(access_token=access_token, token_type="bearer")


@router.post(
    "/",
    response_model=ResponseModel,
    tags=["user"],
    summary="Create User",
)
async def create_user(user: UserCreateDto, db: Session = Depends(get_db)):
    return create(db, user)


@router.delete(
    "/{id}",
    response_model=ResponseDeleteModel,
    tags=["user"],
    summary="Delete User",
)
async def delete_user(id: str, db: Session = Depends(get_db)):
    return delete_by_id(db, id)
