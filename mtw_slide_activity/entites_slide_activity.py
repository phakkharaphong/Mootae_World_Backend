from database_config import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class mtw_slide_activity(Base):
    __tablename__ = "mtw_slide_activity"
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