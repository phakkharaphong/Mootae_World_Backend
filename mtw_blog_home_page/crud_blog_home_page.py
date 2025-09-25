from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session,joinedload
from mtw_blog_home_page import entites_blog_home_page, schema_blog_home_page
from utils.response import PaginatedResponse, Pagination, ResponseDeleteModel, ResponseModel

def FindAll(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    rows = (
        db.query(entites_blog_home_page.mtw_blog_home_page)
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(entites_blog_home_page.mtw_blog_home_page).count()
    respons = [schema_blog_home_page.mtw_blog_home_page.model_validate(vars(r)) for r in rows]
    return PaginatedResponse[schema_blog_home_page.mtw_blog_home_page](
        message="success",
        data=respons,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def updateById(db: Session, id: str, blog_home_page: schema_blog_home_page.update_blog_home_page):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_blog_home_page.mtw_blog_home_page).filter(entites_blog_home_page.mtw_blog_home_page.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="blog not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = blog_home_page.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    blog_home_page_dict = {
        "id": respons.id,
        "blog_title": respons.blog_title,
        "blog_note": respons.blog_note,
        "blog_img_path": respons.blog_img_path,
        "blog_link": respons.blog_link,
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
        data=blog_home_page_dict
    )
    

def getById(db: Session, id: string):
    if id :
       respon = db.query(entites_blog_home_page.mtw_blog_home_page).filter(entites_blog_home_page.mtw_blog_home_page.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="blog not found")

        #แปลง Model Sql Achem to model validate
       respon_data = schema_blog_home_page.mtw_blog_home_page.model_validate(respon)
       return  ResponseModel(
           status=200,
           message="success",
           data=respon_data
       )

def create(db: Session,blog_home_page: schema_blog_home_page.create_blog_home_page):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_blog_home_page = entites_blog_home_page.mtw_blog_home_page(
        id = random_string,
        blog_title = blog_home_page.blog_title,
        blog_note = blog_home_page.blog_note,
        blog_img_path = blog_home_page.blog_img_path,
        blog_link = blog_home_page.blog_link,
        is_active = True,
        created_at = datetime.now(thai_timezone),
        created_by =blog_home_page.created_by)
   # checkid = db.query(entites_aticle_blog.mtw_aticle_blog).filter(entites_aticle_blog.mtw_aticle_blog.id == aricle_blog.id).first()
    
    if not blog_home_page:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_blog_home_page)
        db.commit()
        db.refresh(db_blog_home_page)
    return ResponseModel(
        status=201,
        message="created success",
        data=blog_home_page
    )

def deleteById(db:Session, id: str):
    execute = db.query(entites_blog_home_page.mtw_blog_home_page).filter(entites_blog_home_page.mtw_blog_home_page.id == id).first()
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