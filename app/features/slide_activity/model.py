from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.core.database import Base


class SlideActivity(Base):
    __tablename__ = "slide_activity"

    id = Column(String(50), primary_key=True, index=True)

    title = Column(String(150), index=True)
    img_file_name = Column(String(150))
    img_path = Column(String(150))
    like = Column(Integer)

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
