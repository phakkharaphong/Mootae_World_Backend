from sqlalchemy import Column, DateTime, Integer, String
from database_config import Base
class mtw_attachment (Base):
    __tablename__ = 'mtw_attachment'
    id = Column(String(50), primary_key=True, index=True)
    fileName = Column(String(255))
    content_type = Column(String(255))
    fileLocation = Column(String(255))
    mime = Column(String(30))
    fileSize = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

