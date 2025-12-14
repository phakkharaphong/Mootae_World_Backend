from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Province(Base):
    __tablename__ = "ref_provinces"

    ProvinceId = Column(Integer, primary_key=True, index=True)
    ProvinceNameTH = Column(String(50), index=True)
    ProvinceNameEN = Column(String(50), index=True)
    ZoneId = Column(Integer, ForeignKey("ref_zone.ZoneId"))

    Zone = relationship("Zone", back_populates="Provinces")


class Zone(Base):
    __tablename__ = "ref_zone"

    ZoneId = Column(Integer, primary_key=True, index=True)
    ZoneNameTH = Column(String(50), index=True)
    ZoneNameEN = Column(String(50), index=True)

    Provinces = relationship("Province", back_populates="Zone")