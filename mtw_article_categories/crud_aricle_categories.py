from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from mtw_article_categories import entites_article_categories,schema_article_categories
from utils.response import PaginatedResponse, Pagination, ResponseModel

def FindAll(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entites_article_categories.mtw_article_categories).offset(offset).limit(limit).all()
    total = db.query(entites_article_categories.mtw_article_categories).count()
    # แปลง SQLAlchemy objects เป็น Pydantic
    orders = [schema_article_categories.mtw_article_categories.model_validate(vars(r)) for r in data]

    return PaginatedResponse[schema_article_categories.mtw_article_categories](
        message="success",
        data=orders,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def getById(db: Session, id: string):
    if id :
       respon = db.query(entites_article_categories.mtw_article_categories).filter(entites_article_categories.mtw_article_categories.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="article categories not found")

        #แปลง Model Sql Achem to model validate
       respon_data = schema_article_categories.mtw_article_categories.model_validate(respon)
       return  ResponseModel(
           status=200,
           message="success",
           data=respon_data
       )
    
def create(db: Session,aricle_categories: schema_article_categories.create_mtw_article_categories):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_aricle_categories = entites_article_categories.mtw_article_categories(
        id = random_string,
        name = aricle_categories.name,
        is_active = True,
        created_at = datetime.now(thai_timezone),
        created_by =aricle_categories.created_by)
    checkid = db.query(entites_article_categories.mtw_article_categories).filter(entites_article_categories.mtw_article_categories.id == db_aricle_categories.id).first()
    
    if checkid:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_aricle_categories)
        db.commit()
        db.refresh(db_aricle_categories)
    return ResponseModel(
        status=201,
        message="created success",
        data=aricle_categories
    )

def updateById(db: Session, id: str, aricle_categories: schema_article_categories.update_mtw_article_categories):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_article_categories.mtw_article_categories).filter(entites_article_categories.mtw_article_categories.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="article categories not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = aricle_categories.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    article_categories_dict = {
        "id": respons.id,
        "name": respons.name,
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
        data=article_categories_dict
    )


def deleteById(db:Session, id: str):
    execute = db.query(entites_article_categories.mtw_article_categories).filter(entites_article_categories.mtw_article_categories.id == id).first()
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
