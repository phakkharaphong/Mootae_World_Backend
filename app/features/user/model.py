from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(50), primary_key=True, index=True)

    username = Column(String(100), index=True)
    password = Column(String(100), index=True)
    f_name = Column(String(100), index=True)
    l_name = Column(String(100), index=True)
    phone = Column(String(20), index=True)
    img_profile = Column(String(50), index=True)
    address = Column(String, index=True)
    following = Column(Integer, index=True)
    keep_following = Column(Integer, index=True)

    role_id = Column(String(50), ForeignKey("role.id"))

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    role = relationship("Role", back_populates="users")
