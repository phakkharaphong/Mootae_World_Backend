from sqlalchemy.orm import Session
from mtw_article_categories import entites_article_categories,schema_article_categories
from utils.response import PaginatedResponse, Pagination

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