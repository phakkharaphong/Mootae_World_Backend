from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.features.auth.dto import LoginDto, TokenDto
from app.features.user.dto import UserGetDto
from app.features.user.model import User
from app.utils.password import verify_password

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_current_user(
    token: str = Depends(api_key_header),
    db: Session = Depends(get_db),
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HTTP_401_UNAUTHORIZED",
        )
    
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[settings.HASHING_ALGORITHM],
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload invalid"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = db.query(User).where(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    return user


def require_auth(user: User = Depends(get_current_user)):
    return user


def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required"
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.HASHING_ALGORITHM,
    )
    return encoded_jwt


@router.post(
    "/login",
    response_model=TokenDto,
    tags=["auth"],
    summary="Login for access token",
)
def login_for_access_token(login: LoginDto, db: Session = Depends(get_db)):
    user = db.query(User).where(User.username == login.username).first()
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(data={"sub": user.username})

    return TokenDto(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserGetDto,
    tags=["auth"],
    summary="Get current user info",
)
def get_current_user_info(user: User = Depends(get_current_user)):
    return UserGetDto.model_validate(user)
