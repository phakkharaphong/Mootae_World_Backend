from mtw_orders_type.schema_order_type import mtw_order_type, mtw_order_type_join
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime,date 
import utils
from utils.response import PaginatedResponse

class mtw_order(BaseModel):
    id: str| None = Field(
        description="order id",
        default="EXasfew565d2"
    )
    order_type_id: str |None = Field(
        description="order_type_id",
        default="EXasfew565d2"
    )
    order_type: Optional[mtw_order_type_join] = None
    emphasize_particular: str | None = Field(
        description="emphasize_particular",
        default="Test"
    )
    supplement: str |None = Field(
        description="supplement",
        default="Test Supplement"
    )
    supplement_other: str | None = Field(
        description="supplement_other",
        default="Other"
    )
    birth_date_idol: date |None = Field(
        description="birth_date_idol",
        default=date(2025, 8, 15)
    )

    services_zodiac: bool | None = Field(
        description="services_zodiac",
        default=False
    )
    services_auspicious: bool | None = Field(
        description="services_auspicious",
        default=True
    )
    frist_name_customer: str |None = Field(
        description="Frist Name",
        default="Phakkharaphong"
    )
    last_name_customer: str| None = Field(
        description="Last Name",
        default="Charoenphon"
    )
    birth_date_customer: date |None = Field(
        description="birth_date_customer",
        default=date(2025, 8, 15)
    )
    birth_time_customer: str | None = Field(
        description="birth_time_customer",
        default="08:00"
    )
    gendor: str |None = Field(
        description="Gendor",
        default="male"
    )
    lgbt_description: str | None = Field(
        description="lgbt_description",
        default="LGBTQ ++"
    )
    congenital_disease: str |None = Field(
        description="congenital_disease",
        default="หอบหืด"
    )
    phone: str |None = Field(
        description="phone",
        default="0943955615"
    )
    email: str | None = Field(
        description="email",
        default="example@gmail.com"
    )
    note: str |None = Field(
        description="note",
        default="notentoneotn"
    )
    newsletter: bool |None = Field(
        description="newsletter",
        default=True
    )
    read_accept_pdpa: bool | None  = Field(
        description="read_accept_pdpa",
        default=True
    )
    payment_status: str | None = Field(
        description="payment_status",
        default="รอการชำระเงิน"
    )
    promotion_id: str |None = Field(
        description="promotion_id",
        default="CODE110"
    )
    total_price: float |None = Field(
        description="total_price",
        default=580.00
    )
    is_active: bool | None = None
    created_at: datetime| None = Field(
        description="Created time",
        default=date(2025, 8, 15)
    )
    created_by: str | None = Field(
        description="created by",
        default="Admin"   
    )
    updated_at: datetime | None = None
    updated_by: str | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class mtw_order_create(BaseModel):
    # id: str| None = Field(
    #     description="order id",
    #     default="EXasfew565d2"
    # )
    order_type_id: str |None = Field(
        description="order_type_id",
        default="EXasfew565d2"
    )
    emphasize_particular: str | None = Field(
        description="emphasize_particular",
        default="Work"
    )
    supplement: str |None = Field(
        description="supplement",
        default="ฟรีแลนซ์"
    )
    supplement_other: str | None = Field(
        description="supplement_other",
        default="ฝีมือดีขึ้น ไอเดียบรรเจิด"
    )
    birth_date_idol: date |None = Field(
        description="birth_date_idol",
        default=date(2025, 8, 15)
    )
    services_zodiac: bool | None = Field(
        description="services_zodiac",
        default=True
    )
    services_auspicious: bool | None = Field(
        description="services_auspicious",
        default=True
    )
    frist_name_customer: str |None = Field(
        description="Frist Name",
        default="Phakkharaphong"
    )
    last_name_customer: str| None = Field(
        description="Last Name",
        default="Charoenphon"
    )
    birth_date_customer: date |None = Field(
        description="birth_date_customer",
        default=date(2025, 8, 15)
    )
    birth_time_customer: str | None = Field(
        description="birth_time_customer",
        default="08:00"
    )
    gendor: str |None = Field(
        description="Gendor",
        default="male"
    )
    lgbt_description: str | None = Field(
        description="lgbt_description",
        default="LGBTQ ++"
    )
    congenital_disease: str |None = Field(
        description="congenital_disease",
        default="หอบหืด"
    )
    phone: str |None = Field(
        description="phone",
        default="0943955615"
    )
    email: str | None = Field(
        description="email",
        default="example@gmail.com"
    )
    note: str |None = Field(
        description="note",
        default="notentoneotn"
    )
    newsletter: bool |None = Field(
        description="newsletter",
        default=True
    )
    read_accept_pdpa: bool | None  = Field(
        description="read_accept_pdpa",
        default=True
    )
    promotion_id: str |None = Field(
        description="promotion_id",
        default="CODE110"
    )
    total_price: float |None = Field(
        description="total_price",
        default=580.00
    )
    payment_status: str | None = Field(
        description="Payment Status",
        default="รอการชำระ"
    )
    send_wallpaer_status: str | None = Field(
        description="Send To mail Status",
        default="ยังไม่ดำเนินการ"
    )
    is_active: bool | None = None
    created_at: datetime| None = Field(
        description="Created time",
        default_factory=datetime.now
    )
    created_by: str | None = Field(
        description="created by",
        default="Admin"   
    )
    # updated_at: datetime | None = None
    # updated_by: str | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class mtw_order_update(BaseModel):
    # id: str| None = Field(
    #     description="order id",
    #     default="EXasfew565d2"
    # )
    order_type_id: str |None = Field(
        description="order_type_id",
        default="EXasfew565d2"
    )
    emphasize_particular: str | None = Field(
        description="emphasize_particular",
        default="Work"
    )
    supplement: str |None = Field(
        description="supplement",
        default="ฟรีแลนซ์"
    )
    supplement_other: str | None = Field(
        description="supplement_other",
        default="ฝีมือดีขึ้น ไอเดียบรรเจิด"
    )
    birth_date_idol: date |None = Field(
        description="birth_date_idol",
        default=date(2025, 8, 15)
    )
    services_zodiac: bool | None = Field(
        description="services_zodiac",
        default=True
    )
    services_auspicious: bool | None = Field(
        description="services_auspicious",
        default=True
    )
    frist_name_customer: str |None = Field(
        description="Frist Name",
        default="Phakkharaphong"
    )
    last_name_customer: str| None = Field(
        description="Last Name",
        default="Charoenphon"
    )
    birth_date_customer: date |None = Field(
        description="birth_date_customer",
        default=date(2025, 8, 15)
    )
    birth_time_customer: str | None = Field(
        description="birth_time_customer",
        default="08:00"
    )
    gendor: str |None = Field(
        description="Gendor",
        default="male"
    )
    lgbt_description: str | None = Field(
        description="lgbt_description",
        default="LGBTQ ++"
    )
    congenital_disease: str |None = Field(
        description="congenital_disease",
        default="หอบหืด"
    )
    phone: str |None = Field(
        description="phone",
        default="0943955615"
    )
    email: str | None = Field(
        description="email",
        default="example@gmail.com"
    )
    note: str |None = Field(
        description="note",
        default="notentoneotn"
    )
    newsletter: bool |None = Field(
        description="newsletter",
        default=True
    )
    read_accept_pdpa: bool | None  = Field(
        description="read_accept_pdpa",
        default=True
    )
    promotion_id: str |None = Field(
        description="promotion_id",
        default="CODE110"
    )
    total_price: float |None = Field(
        description="total_price",
        default=580.00
    )
    payment_status: str | None = Field(
        description="Payment Status",
        default="รอการชำระ"
    )
    send_wallpaer_status: str | None = Field(
        description="Send To mail Status",
        default="ยังไม่ดำเนินการ"
    )
    is_active: bool | None = None
    updated_at: datetime| None = Field(
        description="updated time",
        default_factory=datetime.now
    )
    updated_by: str | None = Field(
        description="updated by",
        default="Admin"   
    )
    # updated_at: datetime | None = None
    # updated_by: str | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }


#PaginatedResponse[mtw_order]
# class orderResponse(BaseModel):
#     page: int
#     limit: int
#     total: int
#     message: str
#     Data: List[mtw_order]