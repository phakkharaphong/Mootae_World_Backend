from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(150))
    cover_img = Column(String(150))
    content = Column(Text)
    view = Column(Integer)
    like = Column(Integer)
    
    category_id = Column(String(50), ForeignKey("category.id"), index=True)

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    category = relationship("Category", back_populates="blogs")
