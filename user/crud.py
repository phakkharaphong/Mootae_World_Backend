from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import entitie_user,schema
import random
import string
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

# Load environment variables
load_dotenv()



# ใช้ bcrypt เข้ารหัสรหัสผ่าน
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------------
def verify_password(plain_password):
    return pwd_context.verify(plain_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("REFRESH_SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.ExpiredSignatureError:
        # token หมดอายุ
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": status.HTTP_401_UNAUTHORIZED, 
                "message": "Invalid token"
                },
            headers={
                "WWW-Authenticate": "Bearer"
                },
        )

def getUsername(db: Session,username: str,password: str):
    return db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.username == username, entitie_user.User_entitie.password == password).first()


async def get_current_user(db: Session,
    authorization: str = Header(None),  # อ่านจาก Header Authorization
):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")

    token = authorization[7:]  # ตัด "Bearer "
    username = verify_token(token)  # ฟังก์ชัน decode token ของคุณ
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
# async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
#     username = verify_token(token)
#     if username is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     user = db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


def getById(db: Session, user_id: str):
    return db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.id == user_id).first()

def get_users(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entitie_user.User_entitie).offset(offset).limit(limit).all()
    total = db.query(entitie_user.User_entitie).count()
    # return db.query(models.User).offset(skip).limit(limit).all()
    return {
        "Data": list(data),
        "page": page,
        "limit": limit,
        "total": total,
        "message": "success"
    }

def create_user(db: Session,user: schema.UserCreate):
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_user = entitie_user.User_entitie(id = random_string,
                                        username = user.username,
                                        password = user.password,
                                        f_name = user.f_name,
                                        l_name = user.l_name,
                                        phone = user.phone,
                                        img_profile = user.img_profile,
                                        address = user.address,
                                        following = user.following,
                                        keep_following = user.keep_following,
                                        role_id = user.role_id,
                                        is_active = True,
                                        created_at=datetime.utcnow())
    checkid = db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.id == db_user.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="User ID Invalid")
    else:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def deleteById(db:Session, user_id: str):
    execute = db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.id == user_id).first()
    if not execute:
        return None
    db.delete(execute)
    db.commit()
    return execute