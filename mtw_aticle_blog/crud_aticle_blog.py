from entites_aticle_blog import mtw_aticle_blog
from sqlalchemy.orm import Session,joinedload
def FindAllRole(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    rows = (
        db.query(mtw_aticle_blog)
        .options(joinedload(mtw_aticle_blog.article_categories))  # ✅ join order_type
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(mtw_aticle_blog).count()
    return {
        "Data": list(rows),
        "page": page,
        "limit": limit,
        "total": total,
        "message": "success"
    }