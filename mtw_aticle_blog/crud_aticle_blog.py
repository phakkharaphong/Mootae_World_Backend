from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz
from mtw_aticle_blog import entites_aticle_blog, schema_aticle_blog
from sqlalchemy.orm import Session,joinedload

from utils.response import PaginatedResponse, Pagination, ResponseDeleteModel, ResponseModel
def FindAll(
    db: Session,
    page: int = 0,
    limit: int = 100,
    categories_id: str | None = None,
    keyword: str | None = None,
    is_active: bool | None = None
):
    offset = (page - 1) * limit

    query = db.query(entites_aticle_blog.mtw_aticle_blog).options(
        joinedload(entites_aticle_blog.mtw_aticle_blog.article_categories)
    )
    if keyword:
        query = query.filter(
            entites_aticle_blog.mtw_aticle_blog.title.ilike(f"%{keyword}%")
        )
    if categories_id:
        query = query.filter(
            entites_aticle_blog.mtw_aticle_blog.article_categories_id == categories_id
        )
    if is_active is not None:
        query = query.filter(
            entites_aticle_blog.mtw_aticle_blog.is_active == is_active
        )

    total = query.count()
    rows = query.offset(offset).limit(limit).all()

    respons = [
        schema_aticle_blog.mtw_article_blog.model_validate(vars(r))
        for r in rows
    ]

    return PaginatedResponse[schema_aticle_blog.mtw_article_blog](
        message="success",
        data=respons,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total
        )
    )

def create(db: Session,aricle_blog: schema_aticle_blog.create_mtw_article_blog):
    thai_timezone = pytz.timezone('Asia/Bangkok')
    #Nano ID
    length = 50
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    db_aricle_blog = entites_aticle_blog.mtw_aticle_blog(
        id = random_string,
        title = aricle_blog.title,
        cover_img = aricle_blog.cover_img,
        conten = aricle_blog.conten,
        view = 0,
        like = 0,
        article_categories_id = aricle_blog.article_categories_id,
        is_active = True,
        created_at = datetime.now(thai_timezone),
        created_by =aricle_blog.created_by)
   # checkid = db.query(entites_aticle_blog.mtw_aticle_blog).filter(entites_aticle_blog.mtw_aticle_blog.id == aricle_blog.id).first()
    
    if not aricle_blog:
        raise HTTPException(status_code=404, detail="ID Invalid")
    else:
        db.add(db_aricle_blog)
        db.commit()
        db.refresh(db_aricle_blog)
    return ResponseModel(
        status=201,
        message="created success",
        data=aricle_blog
    )

def getById(db: Session, id: string):
    if id :
       respon = db.query(entites_aticle_blog.mtw_aticle_blog).filter(entites_aticle_blog.mtw_aticle_blog.id == id).first()
       if not respon:
            raise HTTPException(status_code=404, detail="article blog not found")
    respon.view += 1
    db.commit()
    db.refresh(respon)
    respon_data = schema_aticle_blog.mtw_article_blog.model_validate(respon)
    return  ResponseModel(
        status=200,
        message="success",
        data=respon_data
    )
    
def updateById(db: Session, id: str, aticle_blog: schema_aticle_blog.update_mtw_article_blog):
    thai_timezone = pytz.timezone('Asia/Bangkok')

    # 1. หา record เก่า
    respons = db.query(entites_aticle_blog.mtw_aticle_blog).filter(entites_aticle_blog.mtw_aticle_blog.id == id).first()
    if not respons:
        raise HTTPException(status_code=404, detail="aticle blog not found")

    # 2. ดึงเฉพาะ field ที่ส่งมา
    update_data = aticle_blog.model_dump(exclude_unset=True)  # Pydantic v2 ใช้ model_dump()
    
    # 3. อัพเดท field แบบ dynamic
    for key, value in update_data.items():
        setattr(respons, key, value)

    respons.updated_at = datetime.now(thai_timezone)
    article_blog_dict = {
        "id": respons.id,
        "title": respons.title,
        "cover_img": respons.cover_img,
        "conten": respons.conten,
        "view": respons.view,
        "like": respons.like,
        "article_categories_id": respons.article_categories_id,
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
        data=article_blog_dict
    )
    

def deleteById(db:Session, id: str):
    execute = db.query(entites_aticle_blog.mtw_aticle_blog).filter(entites_aticle_blog.mtw_aticle_blog.id == id).first()
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
    

