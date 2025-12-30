from datetime import datetime, date, timezone
from uuid import UUID
from pydantic import BaseModel, Field

from app.features.order_type.dto import OrderTypeGetDto, OrderTypeGetJoinDto
from app.features.promotion.dto import PromotionGetDto, PromotionGetOrderDto


class OrderGetDto(BaseModel):
    id: UUID | None = Field(
        description="order id", 
        default="EXasfew565d2"
    )

    order_type_id: UUID | None = Field(
        description="order_type_id", 
        default="EXasfew565d2"
    )
    order_type: OrderTypeGetJoinDto | None = None

    first_name_customer: str | None = Field(
        description="First Name", 
        default="Phakkharaphong"
    )

    last_name_customer: str | None = Field(
        description="Last Name", 
        default="Charoenphon"
    )

    phone: str | None = Field(
        description="phone", 
        default="0943955615"
    )

    email: str | None = Field(
        description="email", 
        default="example@gmail.com"
    )

    note: str | None = Field(
        description="note", 
        default="notentoneotn"
    )

    birth_date_customer: str | None = Field(
        description="birth_date_customer", 
        default="Monday"
    )

    birth_month_customer: str | None = Field(
        description="birth_month_customer", 
        default="January"
    )

    congenital_disease: str | None = Field(
            description="congenital_disease", 
            default="หอบหืด"
        )
    zodiac_customer: str | None = Field(
        description="Zodiac", 
        default="Rat"
    )
    payment_status: str | None = Field(
        description="payment_status", 
        default="รอการชำระเงิน"
    )

    promotion_id: str | None = Field(
        description="promotion_id", 
        default="CODE110"
    )
    promotion: PromotionGetOrderDto | None = None
    birth_date_customer_number: int | None = Field(
        description="Number for date", 
        default=0
    )
    birth_month_customer_number: int | None = Field(
        description="Number for month", 
        default=0
    )
    zodiac_customer_number: int | None = Field(
        description="Number for zodiac", 
        default=0
    )


    total_price: float | None = Field(
        description="total_price", 
        default=580.00
    )

    is_active: bool | None = Field(
        description="Is Active Category", 
        default=True
    )
    
    created_at: datetime | None = Field(
        description="Created time", 
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    created_by: str | None = Field(
        description="Created by User", 
        default="System"
    )
    
    updated_at: datetime | None = Field(
        description="Updated time", 
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    updated_by: str | None = Field(
        description="Updated by User", 
        default="System"
    )


    model_config = {"from_attributes": True }


class OrderCreateDto(BaseModel):

    order_type_id: str | None = Field(
        description="order_type_id", 
        default="EXasfew565d2"
    )

    first_name_customer: str | None = Field(
        description="First Name", 
        default="Phakkharaphong"
    )

    last_name_customer: str | None = Field(
        description="Last Name", 
        default="Charoenphon"
    )

    phone: str | None = Field(
        description="phone", 
        default="0943955615"
    )

    email: str | None = Field(
        description="email", 
        default="example@gmail.com"
    )

    note: str | None = Field(
        description="note", 
        default="notentoneotn"
    )

    birth_date_customer: str | None = Field(
        description="birth_date_customer", 
        default="Monday"
    )

    birth_month_customer: str | None = Field(
        description="birth_month_customer", 
        default="January"
    )

    congenital_disease: str | None = Field(
        description="congenital_disease", 
        default="หอบหืด"
    )
    zodiac_customer: str | None = Field(
        description="Zodiac", 
        default="Rat"
    )
    payment_status: str | None = Field(
        description="payment_status", 
        default="รอการชำระเงิน"
    )

    promotion_id: str | None = Field(
        description="promotion_id", 
        default="CODE110")

    total_price: float | None = Field(
        description="total_price", 
        default=580.00)


    send_wallpaper_status: str | None = Field(
        description="Send To mail Status", 
        default="ยังไม่ดำเนินการ"
    )

    is_active: bool | None = Field(
        description="Is Active Order", 
        default=True
    )
    
    model_config = {
        "from_attributes": True
    }


class OrderUpdateDto(BaseModel):
    order_type_id: str | None = Field(
        description="order_type_id", 
        default="EXasfew565d2"
    )

    first_name_customer: str | None = Field(
        description="First Name", 
        default="Phakkharaphong"
    )

    last_name_customer: str | None = Field(
        description="Last Name", 
        default="Charoenphon"
    )

    phone: str | None = Field(
        description="phone", 
        default="0943955615"
    )

    email: str | None = Field(
        description="email", 
        default="example@gmail.com"
    )

    note: str | None = Field(
        description="note", 
        default="notentoneotn"
    )

    birth_date_customer: str | None = Field(
        description="birth_date_customer", 
        default="Monday"
    )

    birth_month_customer: str | None = Field(
        description="birth_month_customer", 
        default="January"
    )

    congenital_disease: str | None = Field(
        description="congenital_disease", 
        default="หอบหืด"
    )
    zodiac_customer: str | None = Field(
        description="Zodiac", 
        default="Rat"
    )
    payment_status: str | None = Field(
        description="payment_status", 
        default="รอการชำระเงิน"
    )

    promotion_id: str | None = Field(
        description="promotion_id", 
        default="CODE110")

    total_price: float | None = Field(
        description="total_price", 
        default=580.00)


    send_wallpaper_status: str | None = Field(
        description="Send To mail Status", 
        default="ยังไม่ดำเนินการ"
    )

    is_active: bool | None = Field(
        description="Is Active Order", 
        default=True
    )
    

    model_config = {"from_attributes": True}
