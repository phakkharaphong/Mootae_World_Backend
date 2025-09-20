from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from utils.response import PaginatedResponse, Pagination, ResponseDeleteModel, ResponseModel
from . import entites_promotion,schema_promotion

def FindAll(db: Session, page: int = 1, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(entites_promotion.mtw_promotion)
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(entites_promotion.mtw_promotion).count()

    # แปลง SQLAlchemy → Pydantic
    response = [schema_promotion.mtw_promotion.model_validate(r) for r in rows]

    return PaginatedResponse[schema_promotion.mtw_promotion](
        message="success",
        data=response,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def create(db: Session,promotion: schema_promotion.create_promotion):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_promotion = entites_promotion.mtw_promotion(id = random_string,
                                    promocode = promotion.promocode,
                                    promotion_title = promotion.promotion_title,
                                    start_date = promotion.start_date,
                                    end_date = promotion.end_date,
                                    discount = promotion.discount,
                                    is_active = True,
                                    created_at = datetime.now(thai_timezone),
                                    created_by =promotion.created_by)
    checkid = db.query(entites_promotion.mtw_promotion).filter(entites_promotion.mtw_promotion.id == db_promotion.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_promotion)
        db.commit()
        db.refresh(db_promotion)
    return ResponseModel(
        status=200,
        message="created success",
        data=promotion
    )


def deleteById(db:Session, id: str):
    execute = db.query(entites_promotion.mtw_promotion).filter(entites_promotion.mtw_promotion.id == id).first()
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
def updateById(db: Session, id: str, promotion: schema_promotion.update_promotion):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    db_promotion = db.query(entites_promotion.mtw_promotion).filter(entites_promotion.mtw_promotion.id == id).first()
    if not db_promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = promotion.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(db_promotion, key, value)

    db_promotion.updated_at = datetime.now(thai_timezone)
    promotion_dict = {
        "id": db_promotion.id,
        "promocode": db_promotion.promocode,
        "promotion_title": db_promotion.promotion_title,
        "start_date": db_promotion.start_date,
        "end_date": db_promotion.end_date,
        "discount": db_promotion.discount,
        "is_active": db_promotion.is_active,
        "updated_at": db_promotion.updated_at,
        "updated_by": db_promotion.updated_by
    }


    # 4. commit + refresh
    db.commit()
    db.refresh(db_promotion)

    return ResponseModel(
        status=200,
        message="Updated success",
        data=promotion_dict
    )