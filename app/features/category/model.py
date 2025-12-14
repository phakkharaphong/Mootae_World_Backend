from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(String(50), primary_key=True, index=True)

    name = Column(String(100), unique=True, index=True, nullable=False)

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    blogs = relationship("Blog", back_populates="category")
