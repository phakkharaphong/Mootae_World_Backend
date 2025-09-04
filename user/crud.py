from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import entitie_user,schema
import random
import string

def getById(db: Session, user_id: int):
    return db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.UserID == user_id).first()

def get_users(db: Session, skip:int=0, limit:int=100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(entitie_user.User_entitie).offset(skip).limit(limit).all()

def create_user(db: Session,user: schema.UserCreate):
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_user = entitie_user.User_entitie(UserID = user.UserID,
                                        UserName = user.UserName,
                                        Password = user.Password,
                                        FullName = user.FullName,
                                        Telephone = user.Telephone,
                                        MobilePhone = user.MobilePhone,
                                        IsSuperUser = user.IsSuperUser,
                                        IsActived = user.IsActived,
                                        uid = random_string)
    checkid = db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.UserID == db_user.UserID).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="User ID Invalid")
    else:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def deleteById(db:Session, user_id: int):
    execute = db.query(entitie_user.User_entitie).filter(entitie_user.User_entitie.UserID == user_id).first()
    if not execute:
        return None
    db.delete(execute)
    db.commit()
    return execute