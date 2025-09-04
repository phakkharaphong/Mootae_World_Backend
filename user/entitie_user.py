from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database_config import Base

class User_entitie(Base):
    __tablename__ = "users"
    UserID = Column(
        Integer,
        primary_key=True, 
        index=True
        )
    UserName = Column(String(25),index=True)
    Password = Column(String(255),index=True)
    FullName = Column(String(255),index=True)
    Telephone = Column(String(255),index=True)
    MobilePhone = Column(String(255),index=True)
    uid = Column(String(50),index=True)
    IsSuperUser = Column(Integer,index=True)
    IsActived = Column(Integer,index=True)
