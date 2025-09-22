
from mtw_orders.schema_orders import mtw_order
from mtw_orders.schema_orders import mtw_order_create, mtw_order_update
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
import random
import string
from utils.response import PaginatedResponse, Pagination, ResponseDeleteModel, ResponseModel
from . import entites_orders
from datetime import datetime
import pytz


def FindAll(db: Session, page: int = 1, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(entites_orders.mtw_orders)
        .options(joinedload(entites_orders.mtw_orders.order_type))  # ✅ join order_type
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(entites_orders.mtw_orders).count()

    # แปลง SQLAlchemy → Pydantic
    orders = [mtw_order.model_validate(r) for r in rows]

    return PaginatedResponse[mtw_order](   # ✅ ใช้ mtw_order (schema) ไม่ใช่ data
        message="success",
        data=orders,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def findByEmail(db: Session, email: str,page: int = 1, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(entites_orders.mtw_orders)
        .options(joinedload(entites_orders.mtw_orders.order_type))  # ✅ join 
        .filter(entites_orders.mtw_orders.email == email)
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(entites_orders.mtw_orders).count()
    orders = [mtw_order.model_validate(r) for r in rows]

    return PaginatedResponse[mtw_order](   # ✅ ใช้ mtw_order (schema) ไม่ใช่ data
        message="success",
        data=orders,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def create(db: Session,orders: mtw_order_create):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_orders = entites_orders.mtw_orders(id = random_string,
                                    order_type_id = orders.order_type_id,
                                    emphasize_particular =  orders.emphasize_particular,
                                    supplement = orders.supplement,
                                    supplement_other = orders.supplement_other,
                                    birth_date_idol = orders.birth_date_idol,
                                    services_zodiac = orders.services_zodiac,
                                    services_auspicious = orders.services_auspicious,
                                    frist_name_customer = orders.frist_name_customer,
                                    last_name_customer = orders.last_name_customer,
                                    birth_date_customer = orders.birth_date_customer,
                                    birth_time_customer = orders.birth_time_customer,
                                    gendor = orders.gendor,
                                    lgbt_description = orders.lgbt_description,
                                    congenital_disease = orders.congenital_disease,
                                    phone = orders.phone,
                                    email = orders.email,
                                    note = orders.note,
                                    newsletter = orders.newsletter,
                                    read_accept_pdpa = orders.read_accept_pdpa,
                                    promotion_id = orders.promotion_id,
                                    total_price = orders.total_price,
                                    payment_status  = orders.payment_status,
                                    send_wallpaer_status = orders.send_wallpaer_status,
                                    is_active = True,
                                    created_at = datetime.now(thai_timezone),
                                    created_by =orders.created_by)
    checkid = db.query(entites_orders.mtw_orders).filter(entites_orders.mtw_orders.id == db_orders.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_orders)
        db.commit()
        db.refresh(db_orders)
    return ResponseModel(
        status=200,
        message="created success",
        data=orders
    )
def deleteById(db:Session, id: str):
    execute = db.query(entites_orders.mtw_orders).filter(entites_orders.mtw_orders.id == id).first()
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
def getById(db: Session, id: string):
    if id :
       respon = db.query(entites_orders.mtw_orders).filter(entites_orders.mtw_orders.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="Order id not found")

        #แปลง Model Sql Achem to model validate
       respon_data = mtw_order.model_validate(respon)
       return  ResponseModel(
           status=200,
           message="success",
           data=respon_data
       )
    

def updateById(db: Session, id: str, order: mtw_order_update):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_orders.mtw_orders).filter(entites_orders.mtw_orders.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = order.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    ordertype_dict = {
        "id": respons.id,
        "order_type_id": respons.order_type_id,
        "emphasize_particular": respons.emphasize_particular,
        "supplement": respons.supplement,
        "supplement_other": respons.supplement_other,
        "birth_date_idol": respons.birth_date_idol,
        "services_zodiac": respons.services_zodiac,
        "services_auspicious": respons.services_auspicious,
        "frist_name_customer": respons.frist_name_customer,
        "last_name_customer": respons.last_name_customer,
        "birth_date_customer": respons.birth_date_customer,
        "birth_time_customer": respons.birth_time_customer,
        "gendor": respons.gendor,
        "lgbt_description": respons.lgbt_description,
        "congenital_disease": respons.congenital_disease,
        "phone": respons.phone,
        "email": respons.email,
        "note":respons.note,
        "newsletter":respons.newsletter,
        "read_accept_pdpa":respons.read_accept_pdpa,
        "promotion_id":respons.promotion_id,
        "total_price": respons.total_price,
        "payment_status": respons.payment_status,
        "send_wallpaer_status": respons.send_wallpaer_status,
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