from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
import string
from . import entites_role,schema_role
from datetime import datetime
import pytz

thai_timezone = pytz.timezone('Asia/Bangkok')

def FindAllRole(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entites_role.mtw_role).offset(offset).limit(limit).all()
    total = db.query(entites_role.mtw_role).count()
    return {
        "Data": list(data),
        "page": page,
        "limit": limit,
        "total": total,
        "message": "success"
    }
def create_user(db: Session,role: schema_role.create_mtw_role):
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_role = entites_role.mtw_role(id = random_string,
                                    role_name = role.role_name,
                                    is_active = True,
                                    created_at = datetime.now(thai_timezone),
                                    created_by =role.created_by)
    checkid = db.query(entites_role.mtw_role).filter(entites_role.mtw_role.id == db_role.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="User ID Invalid")
    else:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    return db_role