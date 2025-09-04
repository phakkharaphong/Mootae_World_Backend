from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database_config import Base

class province_base(Base):
    __tablename__ = "ref_provinces"
    ProvinceId = Column(Integer, primary_key=True, index=True)
    ProvinceNameTH = Column(String(50), index=True)
    ProvinceNameEN = Column(String(50), index=True)
    ZoneId = Column(Integer, ForeignKey("ref_zone.ZoneId"))
    
    # Relationship
    Zone = relationship("zone_base", back_populates="Provinces")


class zone_base(Base):
    __tablename__ = "ref_zone"
    ZoneId = Column(Integer, primary_key=True, index=True)
    ZoneNameTH = Column(String(50), index=True)
    ZoneNameEN = Column(String(50), index=True)
    
    # Relationship (one zone -> many provinces)
    Provinces = relationship("province_base", back_populates="Zone")