from datetime import datetime
import random
import string
from typing import Literal, TypeAlias
from fastapi import HTTPException
import pytz
from uuid import UUID
from app.features.order.model import Order
from app.features.order.dto import OrderCreateDto, OrderGetDto, OrderUpdateDto
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session, joinedload

from app.utils.sort import SortOrder

OrderSortField: TypeAlias = Literal["first_name_customer", "last_name_customer", "email", "payment_status","send_wallpaper_status","created_at"]

def find_all(
      db: Session,
      *,
      search: str | None = None,
      sort_by: OrderSortField | None = "created_at",
      sort_order: SortOrder | None = "desc",
      is_active: bool | None = None,
      page: int = 0,
      limit: int = 100,
   ):
    offset = (page - 1) * limit

    query = db.query(Order).options(joinedload(Order.order_type),joinedload(Order.promotion))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
           Order.first_name_customer.ilike(search_term),
           Order.last_name_customer.ilike(search_term),
           Order.email.ilike(search_term),
                             
        )
    if sort_by:
        sort_column = getattr(Order, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(Order.is_active == is_active)

   #  rows = (
   #      db.query(Order)
   #      .options(joinedload(Order.order_type),joinedload(Order.promotion))
   #      .offset(offset)
   #      .limit(limit)
   #      .all()
   #  )
    data = query.offset(offset).limit(limit).all()

    total = query.count()
    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_email(
      db: Session,
      *,
      search: str | None = None,
      sort_by: OrderSortField | None = "created_at",
      sort_order: SortOrder | None = "desc",
      is_active: bool | None = None, 
      email: str, 
      page: int = 0, 
      limit: int = 100
   ):
    offset = (page - 1) * limit
    query = db.query(Order).options(joinedload(Order.order_type),joinedload(Order.promotion)).filter(Order.email == email)
   #  rows = (
   #      db.query(Order)
   #      .options(joinedload(Order.order_type))
   #      .filter(Order.email == email)
   #      .offset(offset)
   #      .limit(limit)
   #      .all()
   #  )
    if search:
        search_term = f"%{search}%"
        query = query.filter(
           Order.first_name_customer.ilike(search_term),
           Order.last_name_customer.ilike(search_term),
           Order.email.ilike(search_term),
                             
        )
    if sort_by:
        sort_column = getattr(Order, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            query = query.order_by(sort_column)

    if is_active is not None:
        query = query.filter(Order.is_active == is_active)


    data = query.offset(offset).limit(limit).all()

    total = query.count()

    return PaginatedResponse(
        message="success",
        data=data,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(
      db: Session, 
      id: UUID
   ):
    if id:
        response = db.query(Order).filter(Order.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="order not found")
        order_get_dto = OrderGetDto.model_validate(vars(response))
        return order_get_dto


def create(
      db: Session, 
      order: OrderCreateDto
   ):
    day_score = 0
    month_score = 0
    zodiac_score = 0
    title_score = 0
    textlist_day = []
    textlist_month = []
    textlist_zodiac = []
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")
    match (order.birth_date_customer):
         case ("Sunday"):
            day_score = 1
         case ("Monday"):
            day_score = 2
         case ("Tuesday"):
            day_score = 3
         case ("Wednesday"):
            day_score = 4
         case ("Thursday"):
            day_score = 5
         case ("Friday"):
            day_score = 6
         case ("Saturday"):
           day_score = 7
         case _:
           day_score = 0

    match order.birth_month_customer:
         case ("November"):
            month_score = 1
         case ("December"):
            month_score = 2
         case ("January"):
            month_score = 3
         case ("February"):
            month_score = 4
         case ("March"):
            month_score = 5
         case ("April"):
            month_score = 6
         case ("May"):
           month_score = 7
         case ("June"):
           month_score = 1
         case ("July"):
           month_score = 2
         case ("August"):
           month_score = 3
         case ("September"):
           month_score = 4
         case ("October"):
           month_score = 5
         case _:
           month_score = 0

    match order.zodiac_customer:
       case ("Rat"):
          zodiac_score = 1
       case ("Ox"):
          zodiac_score = 2
       case ("Tiger"):
          zodiac_score = 3
       case ("Rabbit"):
          zodiac_score = 4
       case ("Dragon"):
          zodiac_score = 5
       case ("Snake"):
          zodiac_score = 6
       case ("Horse"):
          zodiac_score = 7
       case ("Goat"):
          zodiac_score = 1
       case ("Monkey"):
          zodiac_score = 2
       case ("Rooster"):
          zodiac_score = 3
       case ("Dog"):
          zodiac_score = 4
       case ("Pig"):
          zodiac_score = 5
       case _:
          zodiac_score = 0


    match (order.title_moo):
         case ("Love"):
            title_score = random.choice([24, 42, 22, 28, 26])
         case ("Charm"):
            title_score = random.choice([23])
         case ("Travel"):
            title_score = random.choice([27])
         case ("Trade"):
            title_score = random.choice([29])
         case ("Work"):
            title_score = random.choice([45, 46])
         case ("Finance"):
            title_score = random.choice([56, 36, 63])
         case ("Health"):
            title_score = random.choice([46, 45, 59, 95])
         case ("Business"):
            title_score = random.choice([36, 32, 65, 79])
         case _:
            title_score = random.choice([15, 39, 92])

    match day_score:
      case (1):
         textlist_day.extend([4, 5, 9, 0])
      case (2): 
         textlist_day.extend([2, 4, 6, 7, 8, 9, 0])
      case (3):
         textlist_day.extend([2, 4, 5, 6, 9, 0])
      case (4):
         textlist_day.extend([2, 5, 6, 7, 0])
      case (5):
         textlist_day.extend([1, 3, 4, 6, 9, 0])
      case (6):
         textlist_day.extend([2, 3, 4, 5, 0])
      case (7):
         textlist_day.extend([2, 4, 5, 6, 8, 9, 0])
      case (8):
         textlist_day.extend([2, 6, 7, 9, 0])
      case (9):
         textlist_day.extend([1, 2, 3, 4, 5, 6, 7, 8, 0])

    match month_score:
      case (1):
         textlist_month.extend([4, 5, 9, 0])
      case (2): 
         textlist_month.extend([2, 4, 6, 7, 8, 9, 0])
      case (3):
         textlist_month.extend([2, 4, 5, 6, 9, 0])
      case (4):
         textlist_month.extend([2, 5, 6, 7, 0])
      case (5):
         textlist_month.extend([1, 3, 4, 6, 9, 0])
      case (6):
         textlist_month.extend([2, 3, 4, 5, 0])
      case (7):
         textlist_month.extend([2, 4, 5, 6, 8, 9, 0])
      case (8):
         textlist_month.extend([2, 6, 7, 9, 0])
      case (9):
         textlist_month.extend([1, 2, 3, 4, 5, 6, 7, 8, 0])

    match zodiac_score:
      case (1):
         textlist_zodiac.extend([4, 5, 9, 0])
      case (2): 
         textlist_zodiac.extend([2, 4, 6, 7, 8, 9, 0])
      case (3):
         textlist_zodiac.extend([2, 4, 5, 6, 9, 0])
      case (4):
         textlist_zodiac.extend([2, 5, 6, 7, 0])
      case (5):
         textlist_zodiac.extend([1, 3, 4, 6, 9, 0])
      case (6):
         textlist_zodiac.extend([2, 3, 4, 5, 0])
      case (7):
         textlist_zodiac.extend([2, 4, 5, 6, 8, 9, 0])
      case (8):
         textlist_zodiac.extend([2, 6, 7, 9, 0])
      case (9):
         textlist_zodiac.extend([1, 2, 3, 4, 5, 6, 7, 8, 0])
      
    lists = textlist_day + textlist_month +  textlist_zodiac
   #  print("textlist_day: ",textlist_day)
   #  print("textlist_month: ",textlist_month)
   #  print("textlist_zodiac: ",textlist_zodiac)
   #  print("List Is", lists , " and Last :",title_score)
   # #  for i in  textlist_zodiac:
   #  print( day_score,month_score,zodiac_score,title_score," ".join(map(str, lists)),sep=" ")
    full_text = " ".join(map(str, [day_score, month_score, zodiac_score, title_score] + lists))


    new_order = Order(
        order_type_id=order.order_type_id,
        first_name_customer=order.first_name_customer,
        last_name_customer=order.last_name_customer,
        email=order.email,
        phone=order.phone,
        congenital_disease=order.congenital_disease,
        note=order.note,
        title_moo = order.title_moo,
        title_moo_number = title_score,
        birth_date_customer=order.birth_date_customer,
        birth_month_customer=order.birth_month_customer,
        zodiac_customer = order.zodiac_customer,
        full_mootext = full_text,
        promotion_id=order.promotion_id,
        total_price=order.total_price,
        birth_date_customer_number = day_score,
        birth_month_customer_number = month_score,
        zodiac_customer_number = zodiac_score,
        payment_status=order.payment_status,
        send_wallpaper_status=order.send_wallpaper_status,
        is_active=True,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    created_dto = OrderGetDto.model_validate(new_order)
    return ResponseModel(
       status=201, 
       message="Created success", 
       data=created_dto
   )


def update(
      db: Session, 
      id: UUID, 
      order: OrderUpdateDto
   ):

    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(
           status_code=404, 
           detail="order not found"
         )

    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)
    order_dict = {
        "order_type_id": response.order_type_id,
        "first_name_customer": response.first_name_customer,
        "last_name_customer": response.last_name_customer,
        "birth_date_customer": response.birth_date_customer,
        "birth_month_customer": response.birth_month_customer,
        "zodiac_customer": response.zodiac_customer,
        "gender": response.gender,
        "congenital_disease": response.congenital_disease,
        "phone": response.phone,
        "email": response.email,
        "note": response.note,
        "promotion_id": response.promotion_id,
        "total_price": response.total_price,
        "payment_status": response.payment_status,
        "send_wallpaper_status": response.send_wallpaper_status,
        "is_active": response.is_active
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(
       status=200, 
       message="Updated success", 
       data=order_dict
   )


def delete_by_id(
      db: Session, 
      id: UUID
):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    db.delete(response)
    db.commit()

    return ResponseModel(
       status=200, 
       message="Deleted success", 
       data=id
    )
