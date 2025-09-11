from database_config import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class mtw_role(Base):
    __tablename__ = "mtw_role"
    id = Column(String(50), primary_key=True, index=True)
    role_name = Column(String(50), index=True)
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
     # Relationship (one zone -> many provinces)
    User = relationship("User_entitie", back_populates="role")