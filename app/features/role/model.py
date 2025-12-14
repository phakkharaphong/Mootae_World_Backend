from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(String(50), primary_key=True, index=True)

    role_name = Column(String(50), index=True)

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    users = relationship("User", back_populates="role")
