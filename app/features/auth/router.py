from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.features.auth.dto import LoginDto, TokenDto
from app.features.user.dto import UserGetDto
from app.features.user.model import User
from app.utils.password import verify_password

http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    db: Session = Depends(get_db),
):
    if not credentials or not credentials.credentials:
        print("no bearer credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="HTTP_401_UNAUTHORIZED",
        )
    if credentials.scheme.lower() != "bearer":
        print(f"unsupported auth scheme: {credentials.scheme}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unsupported auth scheme",
        )

    token_value = credentials.credentials.strip()
    if token_value.count(".") != 2:
        print("malformed JWT: not enough segments")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed JWT token",
        )

    try:
        payload = jwt.decode(
            token_value,
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[settings.HASHING_ALGORITHM],
        )
        username: str | None = payload.get("sub")
        if username is None:
            print("username not found in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload invalid"
            )
    except JWTError as w:
        print(f"JWTError during token decode: {w}")
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
    tags=["user"],
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
