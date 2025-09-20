
from mtw_orders.schema_orders import mtw_order
from mtw_orders.schema_orders import mtw_order_create
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
import random
import string
from utils.response import PaginatedResponse, Pagination, ResponseModel
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