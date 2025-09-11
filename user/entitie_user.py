from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database_config import Base
from datetime import datetime

class User_entitie(Base):
    __tablename__ = "mtw_users"
    id = Column(
        String,
        primary_key=True, 
        index=True
        )
    username = Column(String(100),index=True)
    password = Column(String(100),index=True)
    f_name = Column(String(100),index=True)
    l_name = Column(String(100),index=True)
    phone = Column(String(20),index=True)
    img_profile = Column(String(50),index=True)
    address = Column(String,index=True)
    following = Column(Integer,index=True)
    keep_following = Column(Integer,index=True)
    role_id = Column(String(50), ForeignKey("mtw_role.id"))
    is_active = Column(Boolean,index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(50), index=True)
    role = relationship("mtw_role", back_populates="User")
