
from sqlalchemy.orm import Session
from fastapi import HTTPException
import random
import string

from utils.response import ResponseDeleteModel, ResponseModel
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
                                    price = order_type.price,
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

def deleteById(db:Session, id: str):
    execute = db.query(entites_order_type.mtw_orders_type).filter(entites_order_type.mtw_orders_type.id == id).first()
    if not execute:
        return None
    elif execute:

        db.delete(execute)
        db.commit()
        return ResponseDeleteModel(
        status=200,
        message="delete success",
        data=id
        )
    
def updateById(db: Session, id: str, order_type: schema_order_type.order_type_update):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_order_type.mtw_orders_type).filter(entites_order_type.mtw_orders_type.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="Order Type not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = order_type.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    ordertype_dict = {
        "id": respons.id,
        "type_name": respons.type_name,
        "price": respons.price,
        "is_active": respons.is_active,
        "updated_at": respons.updated_at,
        "updated_by": respons.updated_by
    }


    # 4. commit + refresh
    db.commit()
    db.refresh(respons)

    return ResponseModel(
        status=200,
        message="Updated success",
        data=ordertype_dict
    )