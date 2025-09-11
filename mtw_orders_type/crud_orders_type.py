
from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
import string
from . import entites_order_type,schema_order_type
from datetime import datetime
import pytz


def FindAll(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entites_order_type.mtw_orders_type).offset(offset).limit(limit).all()
    total = db.query(entites_order_type.mtw_orders_type).count()
    return {
        "Data": list(data),
        "page": page,
        "limit": limit,
        "total": total,
        "message": "success"
    }
def Create(db: Session,order_type: schema_order_type.order_type_create):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_order_type = entites_order_type.mtw_orders_type(id = random_string,
                                    type_name = order_type.type_name,
                                    is_active = True,
                                    created_at = datetime.now(thai_timezone),
                                    created_by =order_type.created_by)
    checkid = db.query(entites_order_type.mtw_orders_type).filter(entites_order_type.mtw_orders_type.id == db_order_type.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_order_type)
        db.commit()
        db.refresh(db_order_type)
    return db_order_type