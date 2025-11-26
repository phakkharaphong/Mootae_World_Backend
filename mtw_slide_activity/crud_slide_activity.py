from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session
from mtw_slide_activity import schema_slide_activity,entites_slide_activity
from utils.response import PaginatedResponse, Pagination, ResponseModel

def FindAll(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entites_slide_activity.mtw_slide_activity).offset(offset).limit(limit).all()
    total = db.query(entites_slide_activity.mtw_slide_activity).count()
    # แปลง SQLAlchemy objects เป็น Pydantic
    orders = [schema_slide_activity.mtw_slide_activity.model_validate(vars(r)) for r in data]

    return PaginatedResponse[schema_slide_activity.mtw_slide_activity](
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
       respon = db.query(entites_slide_activity.mtw_slide_activity).filter(entites_slide_activity.mtw_slide_activity.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="slide not found")

        #แปลง Model Sql Achem to model validate
       respon_data = schema_slide_activity.mtw_slide_activity.model_validate(respon)
       return  ResponseModel(
           status=200,
           message="success",
           data=respon_data
       )
    
def create(db: Session,slide_activity: schema_slide_activity.create_slide_activity):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_slide_activity = entites_slide_activity.mtw_slide_activity(
        id = random_string,
        title = slide_activity.title,
        img_file_name = slide_activity.img_file_name,
        img_path = slide_activity.img_path,
        like = slide_activity.like,
        is_active = True,
        created_at = datetime.now(thai_timezone),
        created_by =slide_activity.created_by)
    #checkid = db.query(entites_footer_website.mtw_footer_website).filter(entites_footer_website.mtw_footer_website.id == footer_website.id).first()
    
    # if checkid:
    #     raise HTTPException(status_code=404, detail="ID Invalid")
    db.add(db_slide_activity)
    db.commit()
    db.refresh(db_slide_activity)
    return ResponseModel(
        status=201,
        message="created success",
        data=slide_activity
    )


def updateById(db: Session, id: str, slide_activity: schema_slide_activity.update_slide_activity):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    respons = db.query(entites_slide_activity.mtw_slide_activity).filter(entites_slide_activity.mtw_slide_activity.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="slide not found")
    update_data = slide_activity.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    slide_activity_dict = {
        "id": respons.id,
        "title": respons.title,
        "img_file_name": respons.img_file_name,
        "img_path": respons.img_path,
        "like": respons.like,
        "is_active": respons.is_active,
        "updated_at": respons.updated_at,
        "updated_by": respons.updated_by
    }


    db.commit()
    db.refresh(respons)

    return ResponseModel(
        status=200,
        message="Updated success",
        data=slide_activity_dict
    )


def deleteById(db:Session, id: str):
    execute = db.query(entites_slide_activity.mtw_slide_activity).filter(entites_slide_activity.mtw_slide_activity.id == id).first()
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
