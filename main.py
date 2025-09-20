from typing import Annotated, Union
from enum import Enum
from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from database_config import SessionLocal
from user import crud
from mtw_role import crud_role
from mtw_orders_type import crud_orders_type
from Location import crud_location
import user.schema as schemas
import mtw_orders_type.schema_order_type as schema_order_type
import mtw_role.schema_role as schema_role
import Location.schema_location as schemas_location
import database_config as db_con
import mtw_orders.schema_orders as schema_order
from mtw_orders import crud_order
from utils import response
from mtw_promotion import schema_promotion, crud_promotion

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
        response_model=schemas.UsersResponse ,
        tags=["User"],
        summary="Find All User"
        )
def get_users(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    users = crud.get_users(db,page=page,limit=limit)
    return users

@app.get(
        "/user/{user_id}",
        response_model=schemas.UserSchema ,
        tags=["User"],
        summary="Get User By ID"
        )
async def get_userbyid(
    user_id: str, 
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
    user_id: str,
    db: Session = Depends(get_db)
):
    user = crud.deleteById(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=200, detail=f"Delete User Success: {user.id}")


@app.get(
        "/role", 
        response_model=schema_role.RoleResponse ,
        tags=["Role"],
        summary="Find All Role"
        )
def get_role(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    role = crud_role.FindAllRole(db,page=page,limit=limit)
    return role
@app.post("/role/create",response_model=schema_role.create_mtw_role ,tags=["Role"])
async def create_role(role:schema_role.create_mtw_role, db:Session=Depends(get_db)):
    return crud_role.create_user(db=db,role=role)



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


@app.get(
        "/order_types", 
        response_model=schema_order_type.order_type_Response ,
        tags=["Order Type"],
        summary="Find All Order Type"
        )
async def getall_Oder_Type(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    rders_type = crud_orders_type.FindAll(db,page=page,limit=limit)
    return rders_type

@app.post(
        "/order_types/create",
        response_model=schema_order_type.order_type_create ,
        tags=["Order Type"]
        )
async def create_order_type(order_type: schema_order_type.order_type_create, db: Session = Depends(get_db)):
    return crud_orders_type.Create(db=db, order_type=order_type)

@app.get(
        "/promotions", 
        response_model=response.PaginatedResponse[schema_promotion.mtw_promotion] ,
        tags=["Promotion"],
        summary="Find All Promotions"
        )
async def findall_Promotion(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    response = crud_promotion.FindAll(db,page=page,limit=limit)
    return response

@app.post(
        "/promotion/create",
        response_model=response.ResponseModel ,
        tags=["Promotion"]
        )
async def create_promotion(promotion: schema_promotion.create_promotion, db: Session = Depends(get_db)):
    print(promotion)
    return crud_promotion.create(db=db, promotion=promotion)
@app.patch(
    "/promotion/{id}",
    response_model=response.ResponseModel ,
    tags=["Promotion"]
)
async def update_promotion(promotion: schema_promotion.update_promotion,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_promotion.updateById(db=db, id=id, promotion=promotion)


@app.delete(
    "/promotion/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Promotion"]
)
async def delete_promotion(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_promotion.deleteById(db=db, id=id)
    return response
    # if not response:
    #     raise HTTPException(status_code=404, detail="response not found")
    # else:
    #     raise HTTPException(status_code=200, detail=f"Delete response Success: {response.id}")

@app.get(
        "/orders", 
        response_model=response.PaginatedResponse[schema_order.mtw_order] ,
        tags=["Orders"],
        summary="Find All Orders"
        )
async def getall_Oders(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
    ):
    order_response = crud_order.FindAll(db,page=page,limit=limit)
    return order_response

@app.post(
        "/orders/create",
        response_model=response.ResponseModel ,
        tags=["Orders"]
        )
async def create_orders(orders: schema_order.mtw_order_create, db: Session = Depends(get_db)):
    print(orders)
    return crud_order.create(db=db, orders=orders)
