from sqlalchemy import Boolean, Column, DateTime, String, Text, Date,Integer, ForeignKey
from sqlalchemy.orm import relationship
from database_config import Base


class mtw_aticle_blog(Base):
    __tablename__ = "mtw_aticle_blog"   # แก้จาก mtw_aticle_blog
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(150))
    cover_img = Column(String(150))
    conten = Column(Text)
    view = Column(Integer)
    like = Column(Integer)
    article_categories_id = Column(String(50), ForeignKey("mtw_article_categories.id"), index=True)
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    article_categories = relationship("mtw_article_categories", back_populates="article_blog")