from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from . import entitie_user,schema
import random
import string

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