from typing import Annotated
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
import mtw_orders.schema_orders as schema_order
from mtw_orders import crud_order
from utils import response
from mtw_promotion import schema_promotion, crud_promotion
from mtw_slide_new import schema_slide_new, crud_slide_new
from mtw_aticle_blog import entites_aticle_blog,crud_aticle_blog,schema_aticle_blog
from mtw_article_categories import schema_article_categories,crud_aricle_categories,entites_article_categories
from mtw_blog_home_page import schema_blog_home_page, crud_blog_home_page , entites_blog_home_page

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


#========================== User Tag ==========================
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
    
#========================== Role Tag ==========================

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

#========================== Location Tag ==========================

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


#========================== Order Types Tag ==========================

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
@app.delete(
    "/order_type/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Order Type"]
)
async def deleteOdertype(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_orders_type.deleteById(db=db, id=id)
    return response

@app.patch(
    "/order_type/{id}",
    response_model=response.ResponseModel ,
    tags=["Order Type"]
)
async def updateOrderType(order_type: schema_order_type.order_type_update,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_orders_type.updateById(db=db, id=id, order_type=order_type)


#========================== Promotion Tag ==========================

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

#========================== Orders Tag ==========================
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

@app.get(
    "/order/{id}",
    response_model=response.ResponseModel,
    tags=["Orders"],
    summary="getBy Id Order"
)
async def getByIdOrder(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_order.getById(db=db, id=id)
    return response

@app.get(
        "/ordersByEmail/",
        response_model=response.PaginatedResponse[schema_order.mtw_order] ,
        tags=["Orders"],
        summary="Find Orders By Email"
)
async def findOrderByEmail(
    email: str,
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
):
    response_data = crud_order.findByEmail(db=db, email=email, page=page, limit=limit)
    return response_data


@app.post(
        "/orders/create",
        response_model=response.ResponseModel ,
        tags=["Orders"]
        )
async def create_orders(orders: schema_order.mtw_order_create, db: Session = Depends(get_db)):
    print(orders)
    return crud_order.create(db=db, orders=orders)

@app.delete(
    "/orders/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Orders"]
)
async def deleteOrder(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_order.deleteById(db=db, id=id)
    return response

@app.patch(
    "/orders/{id}",
    response_model=response.ResponseModel ,
    tags=["Orders"]
)
async def updateOrder(order: schema_order.mtw_order_update,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_order.updateById(db=db, id=id, order=order)

#========================== Slide New Tag ==========================

@app.get(
        "/slidenew",
        response_model=response.PaginatedResponse[schema_slide_new.mtw_slide_new] ,
        tags=["Slidenew"],
        summary="Find Slidenew"
)
async def findSlidenew(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
):
    response_data = crud_slide_new.FindAll(db=db, page=page, limit=limit)
    return response_data
@app.get(
    "/slidenew/{id}",
    response_model=response.ResponseModel,
    tags=["Slidenew"],
    summary="getBy Id SlideNew"
)
async def getByIdSlideNew(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_slide_new.getById(db=db, id=id)
    return response

@app.post(
        "/slidenew/create",
        response_model=response.ResponseModel ,
        tags=["Slidenew"],
        summary="Create Slidenew"
        )
async def create_slide_new(slide_new: schema_slide_new.create_mtw_slide_new, db: Session = Depends(get_db)):
    print(slide_new)
    return crud_slide_new.create(db=db, slide_new=slide_new)

@app.patch(
    "/slidenew/{id}",
    response_model=response.ResponseModel ,
    tags=["Slidenew"],
    summary="Update Slidenew"
)
async def updateSlidenew(slide_new: schema_slide_new.update_mtw_slide_new,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_slide_new.updateById(db=db, id=id, slide_new=slide_new)

@app.delete(
    "/slidenew/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Slidenew"],
    summary="Delete Slidenew"
)
async def deleteSlideNew(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_slide_new.deleteById(db=db, id=id)
    return response
#========================== Article Categories Tag ==========================

@app.get(
        "/articlecategories/",
        response_model=response.PaginatedResponse[schema_article_categories.mtw_article_categories] ,
        tags=["Article Categories"],
        summary="Find Article Categories"
)
async def findArticleCategories(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
):
    response_data = crud_aricle_categories.FindAll(db=db, page=page, limit=limit)
    return response_data

@app.get(
    "/articlecategories/{id}",
    response_model=response.ResponseModel,
    tags=["Article Categories"],
    summary="getBy Id Article Categories"
)
async def getByIdArticleCategories(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_aricle_categories.getById(db=db, id=id)
    return response

@app.post(
        "/articlecategories/create",
        response_model=response.ResponseModel ,
        tags=["Article Categories"],
        summary="Create Article Categories"
        )
async def create_article_categories(aricle_categories: schema_article_categories.create_mtw_article_categories, db: Session = Depends(get_db)):
    print(aricle_categories)
    return crud_aricle_categories.create(db=db, aricle_categories=aricle_categories)

@app.patch(
    "/articlecategories/{id}",
    response_model=response.ResponseModel ,
    tags=["Article Categories"],
    summary="Update Article Categories"
)
async def update_article_categories(aricle_categories: schema_article_categories.update_mtw_article_categories,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_aricle_categories.updateById(db=db, id=id, aricle_categories=aricle_categories)

@app.delete(
    "/articlecategories/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Article Categories"],
    summary="Delete Article Categories"
)
async def deleteArticleCategories(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_aricle_categories.deleteById(db=db, id=id)
    return 

#========================== Article Blog Tag ==========================

@app.get(
        "/articleblog/",
        response_model=response.PaginatedResponse[schema_aticle_blog.mtw_article_blog] ,
        tags=["Article Blog"],
        summary="Find Article Blog"
)
async def findArticleBlog(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
):
    response_data = crud_aticle_blog.FindAll(db=db, page=page, limit=limit)
    return response_data

@app.get(
    "/articleblog/{id}",
    response_model=response.ResponseModel,
    tags=["Article Blog"],
    summary="getBy id Article Blog"
)
async def getByIdArticleblog(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_aticle_blog.getById(db=db, id=id)
    return response

@app.patch(
    "/articleblog/{id}",
    response_model=response.ResponseModel ,
    tags=["Article Blog"],
    summary="Update Article Blog"
)
async def update_article_blog(aticle_blog: schema_aticle_blog.update_mtw_article_blog,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_aticle_blog.updateById(db=db, id=id, aticle_blog=aticle_blog)


@app.post(
        "/articleblog/create",
        response_model=response.ResponseModel ,
        tags=["Article Blog"],
        summary="Create Article Blog"
        )
async def create_article_blog(aricle_blog: schema_aticle_blog.create_mtw_article_blog, db: Session = Depends(get_db)):
    print(aricle_blog)
    return crud_aticle_blog.create(db=db, aricle_blog=aricle_blog)



@app.delete(
    "/articleblog/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Article Blog"],
    summary="Delete Article Blog"
)
async def deleteArticleBlog(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_aticle_blog.deleteById(db=db, id=id) 
    return  response


#=========================== blog home page ====================

@app.get(
        "/bloghomepage/",
        response_model=response.PaginatedResponse[schema_blog_home_page.mtw_blog_home_page] ,
        tags=["Blog Home Page"],
        summary="Find Blog home page"
)
async def findBlogHomePage(
    page:int=1, 
    limit:int=10, 
    db:Session=Depends(get_db)
):
    response_data = crud_blog_home_page.FindAll(db=db, page=page, limit=limit)
    return response_data


@app.get(
    "/bloghomepage/{id}",
    response_model=response.ResponseModel,
    tags=["Blog Home Page"],
    summary="getBy id Blog Home Page"
)
async def getById_blog_home_page(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_blog_home_page.getById(db=db, id=id)
    return response

@app.post(
        "/bloghomepage/create",
        response_model=response.ResponseModel ,
        tags=["Blog Home Page"],
        summary="Create Blog Home Page"
        )
async def create_blog_home_page(blog_home_page: schema_blog_home_page.create_blog_home_page, db: Session = Depends(get_db)):
    print(blog_home_page)
    return crud_blog_home_page.create(db=db, blog_home_page=blog_home_page)


@app.patch(
    "/bloghomepage/{id}",
    response_model=response.ResponseModel ,
    tags=["Blog Home Page"],
    summary="Update Blog Home Page"
)
async def update_blog_home_page(blog_home_page: schema_blog_home_page.update_blog_home_page,id: str, db: Session = Depends(get_db)):
    print(id)
    return crud_blog_home_page.updateById(db=db, id=id, blog_home_page=blog_home_page)

@app.delete(
    "/bloghomepage/{id}",
    response_model=response.ResponseDeleteModel,
    tags=["Blog Home Page"],
    summary="Delete Blog Home Page"
)
async def delete_blog_home_page(
    id: str,
    db: Session = Depends(get_db)
):
    response =  crud_blog_home_page.deleteById(db=db, id=id) 
    return  response
