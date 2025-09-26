from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from mtw_footer_website import entites_footer_website, schema_footer_website
from utils.response import PaginatedResponse, Pagination, ResponseModel

def FindAll(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entites_footer_website.mtw_footer_website).offset(offset).limit(limit).all()
    total = db.query(entites_footer_website.mtw_footer_website).count()
    # แปลง SQLAlchemy objects เป็น Pydantic
    orders = [schema_footer_website.mtw_footer_website.model_validate(vars(r)) for r in data]

    return PaginatedResponse[schema_footer_website.mtw_footer_website](
        message="success",
        data=orders,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def getById(db: Session, id: str):
    if id :
       respon = db.query(entites_footer_website.mtw_footer_website).filter(entites_footer_website.mtw_footer_website.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="footer not found")

        #แปลง Model Sql Achem to model validate
       respon_data = schema_footer_website.mtw_footer_website.model_validate(respon)
       return  ResponseModel(
           status=200,
           message="success",
           data=respon_data
       )
    
def create(db: Session,footer_website: schema_footer_website.create_footer_website):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_footer_website = entites_footer_website.mtw_footer_website(
        id = random_string,
        title = footer_website.title,
        icon_img = footer_website.icon_img,
        link_ref = footer_website.link_ref,
        is_active = True,
        created_at = datetime.now(thai_timezone),
        created_by =footer_website.created_by)
    #checkid = db.query(entites_footer_website.mtw_footer_website).filter(entites_footer_website.mtw_footer_website.id == footer_website.id).first()
    
    # if checkid:
    #     raise HTTPException(status_code=404, detail="ID Invalid")
    db.add(db_footer_website)
    db.commit()
    db.refresh(db_footer_website)
    return ResponseModel(
        status=201,
        message="created success",
        data=footer_website
    )


def updateById(db: Session, id: str, footer_website: schema_footer_website.update_footer_website):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_footer_website.mtw_footer_website).filter(entites_footer_website.mtw_footer_website.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="footer icon not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = footer_website.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    footer_website_dict = {
        "id": respons.id,
        "title": respons.title,
        "icon_img": respons.icon_img,
        "link_ref": respons.link_ref,
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
        data=footer_website_dict
    )


def deleteById(db:Session, id: str):
    execute = db.query(entites_footer_website.mtw_footer_website).filter(entites_footer_website.mtw_footer_website.id == id).first()
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
