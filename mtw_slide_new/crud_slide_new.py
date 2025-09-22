from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from mtw_slide_new import entites_slide_new,schema_slide_new
from utils.response import PaginatedResponse, Pagination, ResponseByIdModel, ResponseDeleteModel, ResponseModel  # <-- แก้ชื่อให้ตรงไฟล์จริง

def FindAll(db: Session, page: int = 1, limit: int = 100):
    offset = (page - 1) * limit
    data = db.query(entites_slide_new.mtw_slide_new).offset(offset).limit(limit).all()
    total = db.query(entites_slide_new.mtw_slide_new).count()
    
    # แปลง SQLAlchemy objects เป็น Pydantic
    orders = [schema_slide_new.mtw_slide_new.model_validate(vars(r)) for r in data]

    return PaginatedResponse[schema_slide_new.mtw_slide_new](
        message="success",
        data=orders,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def create(db: Session,slide_new: schema_slide_new.create_mtw_slide_new):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_slide_new = entites_slide_new.mtw_slide_new(
        id = random_string,
        title = slide_new.title,
        link_ref = slide_new.link_ref,
        img_path = slide_new.img_path,
        slide_number = slide_new.slide_number,
        is_active = True,
        created_at = datetime.now(thai_timezone),
        created_by =slide_new.created_by)
    checkid = db.query(entites_slide_new.mtw_slide_new).filter(entites_slide_new.mtw_slide_new.id == db_slide_new.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_slide_new)
        db.commit()
        db.refresh(db_slide_new)
    return ResponseModel(
        status=201,
        message="created success",
        data=slide_new
    )

def getById(db: Session, id: string):
    if id :
       respon = db.query(entites_slide_new.mtw_slide_new).filter(entites_slide_new.mtw_slide_new.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="Slide not found")

        #แปลง Model Sql Achem to model validate
       respon_data = schema_slide_new.mtw_slide_new.model_validate(respon)
       return  ResponseModel(
           status=200,
           message="success",
           data=respon_data
       )
def deleteById(db:Session, id: str):
    execute = db.query(entites_slide_new.mtw_slide_new).filter(entites_slide_new.mtw_slide_new.id == id).first()
    if not execute:
        return None
    elif execute:

        db.delete(execute)
        db.commit()
        return ResponseModel(
        status=200,
        message="delete success",
        data=id
        )
    
def updateById(db: Session, id: str, slide_new: schema_slide_new.update_mtw_slide_new):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_slide_new.mtw_slide_new).filter(entites_slide_new.mtw_slide_new.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="Slide not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = slide_new.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    ordertype_dict = {
        "id": respons.id,
        "title": respons.title,
        "link_ref": respons.link_ref,
        "img_path": respons.img_path,
        "slide_number": respons.slide_number,
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