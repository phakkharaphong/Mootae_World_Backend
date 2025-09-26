from sqlalchemy import Boolean, Column, DateTime, String, Text, Date,Integer
from database_config import Base


class mtw_footer_website(Base):
    __tablename__ = "mtw_footer_website"
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(150), index=True)
    icon_img = Column(String(100))
    link_ref = Column(String(100))
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
     # Relationship (one zone -> many provinces)
    #User = relationship("User_entitie", back_populates="role")
