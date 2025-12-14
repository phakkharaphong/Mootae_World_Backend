from sqlalchemy import Boolean, Column, DateTime, String
from app.core.database import Base


class BlogHomepage(Base):
    __tablename__ = "blog_home_page"

    id = Column(String(50), primary_key=True, index=True)

    title = Column(String(200))
    note = Column(String(150))
    img_path = Column(String(150))
    link = Column(String(150))

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
