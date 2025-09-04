from typing import Annotated, Union
from enum import Enum
from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from database_config import SessionLocal
from user import crud
from Location import crud_location
import user.schema as schemas
import Location.schema_location as schemas_location

app = FastAPI(
    title="Mootae World API Doccument",
        description="This is a API Docuemtn Project Mootae World API.",
        version="1.0.0",
        contact={
            "name": "API Support",
            "url": "http://example.com/contact",
            "email": "phakkharaphong.c@kkumail.com",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]

#ในกรณีถ้าต้องการดึงข้อมูลหลายเรคคอร์ดให้ใช้ List
@app.get(
        "/users", 
        response_model=list[schemas.UserSchema] ,
        tags=["User"],
        summary="Find All User"
        )
def get_users(
    skip:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users

@app.get(
        "/user/{user_id}",
        response_model=schemas.UserSchema ,
        tags=["User"],
        summary="Get User By ID"
        )
async def get_userbyid(
    user_id: int, 
    db:Session=Depends(get_db)
    ):
    user = crud.getById(db,user_id=user_id)
    return user

@app.post("/users",response_model=schemas.UserCreate ,tags=["User"])
async def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    # #db_user = crud.create_user(db,
    #                            UserID=user.UserID,
    #                            UserName=user.UserName,
    #                            Password=user.Password,
    #                            FullName=user.FullName,
    #                            Telephone=user.Telephone,
    #                            MobilePhone=user.MobilePhone)
    return crud.create_user(db=db,user=user)

@app.delete(
    "/delete/user/{user_id}",
    response_model=schemas.UserSchema,
    tags=["User"]
)
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = crud.deleteById(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=200, detail=f"Delete User Success: {user.UserName}")

@app.get(
        "/location/province", 
        response_model=schemas_location.ProvinceResponse,
        tags=["Location"],
        summary="Find All Province"
        )
def get_province(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    users = crud_location.FindAllProvince(db,page=page,limit=limit)
    return users
@app.get(
        "/location/province/{ProvinceId}", 
        response_model=schemas_location.province, 
        tags=["Location"],
        description="Get Province By id",
        summary="Get Province By id"
        )
def getProvinceById(
    ProvinceId: int, 
    db:Session=Depends(get_db)
    ):
    Province = crud_location.getById(db=db,ProvinceId=ProvinceId)
    return Province

@app.get(
        "/Location/Zone",
        response_model=schemas_location.ZoneResponse,
        tags=["Location"],
        description="Get All Location",
        summary="Get All Location",
    )
def FindAllZone(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    return crud_location.FindAllZone(db,page,limit)


