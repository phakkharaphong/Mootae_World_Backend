from sqlalchemy.orm import Session

from . import entities_location, schema_location

def getById(db: Session, ProvinceId: int):
    return db.query(entities_location.province_base).filter(entities_location.province_base.ProvinceId == ProvinceId).first()

def FindAllProvince(db: Session, page:int=0, limit:int=100):
    offset = (page - 1) * limit
    data = db.query(entities_location.province_base).offset(offset).limit(limit).all()
    total = db.query(entities_location.province_base).count()
    return {
        "Data": list(data),
        "page": page,
        "limit": limit,
        "total": total,
        "message": "success"
    }

def FindAllZone(db: Session, page:int, limit: int=0):
    offset = (page - 1) * limit
    data = db.query(entities_location.zone_base).offset(offset).limit(limit).all()
    total = db.query(entities_location.zone_base).count()
    return {
        "Data": list(data),
        "page": page,
        "limit": limit,
        "total": total,
        "message": "success"
    }


# def create_user(db: Session,user: schema.UserCreate):
#     db_user = entities_ref_provinces.User_entitie(UserID = user.UserID,
#                                         UserName = user.UserName,
#                                         Password = user.Password,
#                                         FullName = user.FullName,
#                                         Telephone = user.Telephone,
#                                         MobilePhone = user.MobilePhone,
#                                         IsSuperUser = user.IsSuperUser,
#                                         IsActived = user.IsActived)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
