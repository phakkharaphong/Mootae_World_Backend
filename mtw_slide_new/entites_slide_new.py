from sqlalchemy import Boolean, Column, DateTime, String, Text, Date,Integer
from database_config import Base


class mtw_slide_new(Base):
    __tablename__ = "mtw_slide_new"
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(150), index=True)
    link_ref = Column(String(100))
    img_path = Column(String(200))
    slide_number = Column(Integer)
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
     # Relationship (one zone -> many provinces)
    #User = relationship("User_entitie", back_populates="role")
