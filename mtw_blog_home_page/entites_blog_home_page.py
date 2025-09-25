from sqlalchemy import Boolean, Column, DateTime, String, Text, Date,Integer, ForeignKey
from sqlalchemy.orm import relationship
from database_config import Base


class mtw_blog_home_page(Base):
    __tablename__ = "mtw_blog_home_page"   # mtw_blog_home_page
    id = Column(String(50), primary_key=True, index=True)
    blog_title = Column(String(200))
    blog_note = Column(String(150))
    blog_img_path = Column(String(150))
    blog_link = Column(String(150))
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)