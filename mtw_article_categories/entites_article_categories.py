from sqlalchemy import Boolean, Column, DateTime, String, Text, Date,Integer
from pydantic import Field
from sqlalchemy.orm import relationship
from database_config import Base


class mtw_article_categories(Base):
    __tablename__ = "mtw_article_categories"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100))
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    article_blog = relationship("mtw_aticle_blog", back_populates="article_categories")


