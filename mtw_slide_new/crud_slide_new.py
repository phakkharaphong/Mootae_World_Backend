from sqlalchemy.orm import Session
from mtw_slide_new import entites_slide_new,schema_slide_new
from utils.response import PaginatedResponse, Pagination  # <-- แก้ชื่อให้ตรงไฟล์จริง

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
