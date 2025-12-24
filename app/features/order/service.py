from datetime import datetime
import random
import string
from fastapi import HTTPException
import pytz

from app.features.order.model import Order
from app.features.order.dto import OrderCreateDto, OrderGetDto, OrderUpdateDto
from app.utils.response import PaginatedResponse, Pagination, ResponseModel
from sqlalchemy.orm import Session, joinedload


def find_all(db: Session, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(Order)
        .options(joinedload(Order.order_type),joinedload(Order.promotion))
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(Order).count()
    orders = [OrderGetDto.model_validate(r) for r in rows]
    return PaginatedResponse[OrderGetDto](
        message="success",
        data=orders,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_email(db: Session, email: str, page: int = 0, limit: int = 100):
    offset = (page - 1) * limit
    rows = (
        db.query(Order)
        .options(joinedload(Order.order_type))
        .filter(Order.email == email)
        .offset(offset)
        .limit(limit)
        .all()
    )
    total = db.query(Order).count()
    orders = [OrderGetDto.model_validate(r) for r in rows]
    return PaginatedResponse[OrderGetDto](
        message="success",
        data=orders,
        pagination=Pagination(page=page, limit=limit, total=total),
    )


def find_by_id(db: Session, id: str):
    if id:
        response = db.query(Order).filter(Order.id == id).first()
        if not response:
            raise HTTPException(status_code=404, detail="order not found")
        order_get_dto = OrderGetDto.model_validate(vars(response))
        return order_get_dto


def create(db: Session, order: OrderCreateDto):
    day_score = 0
    month_score = 0
    zodiac_score = 0
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
    thai_timezone = pytz.timezone("Asia/Bangkok")
    length = 50
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
   

    new_order = Order(
        id=random_string,
        order_type_id=order.order_type_id,
        first_name_customer=order.first_name_customer,
        last_name_customer=order.last_name_customer,
        email=order.email,
        phone=order.phone,
        congenital_disease=order.congenital_disease,
        note=order.note,
        birth_date_customer=order.birth_date_customer,
        birth_month_customer=order.birth_month_customer,
        zodiac_customer = order.zodiac_customer,
        promotion_id=order.promotion_id,
        total_price=order.total_price,
        birth_date_customer_number = day_score,
        birth_month_customer_number = month_score,
        zodiac_customer_number = zodiac_score,
        payment_status=order.payment_status,
        send_wallpaper_status=order.send_wallpaper_status,
        is_active=True,
        created_at=datetime.now(thai_timezone),
        created_by=order.created_by,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    created_dto = OrderGetDto.model_validate(new_order)
    return ResponseModel(status=201, message="Created success", data=created_dto)


def update_by_id(db: Session, id: str, order: OrderUpdateDto):
    thai_timezone = pytz.timezone("Asia/Bangkok")

    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(response, key, value)

    response.updated_at = datetime.now(thai_timezone)
    order_dict = {
        "id": response.id,
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
        "is_active": response.is_active,
        "updated_at": response.updated_at,
        "updated_by": response.updated_by,
    }

    db.commit()
    db.refresh(response)

    return ResponseModel(status=200, message="Updated success", data=order_dict)


def delete_by_id(db: Session, id: str):
    response = db.query(Order).filter(Order.id == id).first()
    if not response:
        raise HTTPException(status_code=404, detail="order not found")

    db.delete(response)
    db.commit()

    return ResponseModel(status=200, message="Deleted success", data={"id": id})
