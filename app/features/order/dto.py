from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field

from app.features.order_type.dto import OrderTypeGetJoinDto


class OrderGetDto(BaseModel):
    id: UUID | None = Field(description="order id", examples=["EXasfew565d2"])

    order_type_id: UUID | None = Field(
        description="order_type_id", examples=["EXasfew565d2"]
    )
    order_type: OrderTypeGetJoinDto | None = None

    first_name_customer: str | None = Field(
        description="First Name", examples=["Phakkharaphong"]
    )

    last_name_customer: str | None = Field(
        description="Last Name", examples=["Charoenphon"]
    )

    phone: str | None = Field(description="phone", examples=["0943955615"])

    email: str | None = Field(description="email", examples=["example@gmail.com"])

    wallpaper_url: str| None = Field(
        description="wallpaper URL",
        examples=["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSD5EUXKEZYWRihvBte-enLd1V8C0OPK6lXKg&s"]
    )
    full_mootext: str| None = Field(
        description="full_mootext",
        examples=["2 1 4 24"]
    )


    payment_status: str | None = Field(
        description="payment_status", examples=["รอการชำระเงิน"]
    )

    birth_date_customer_number: int | None = Field(
        description="Number for date", examples=[0]
    )

    birth_month_customer_number: int | None = Field(
        description="Number for month", examples=[0]
    )

    zodiac_customer_number: int | None = Field(
        description="Number for zodiac", examples=[0]
    )

    total_price: float | None = Field(description="total_price", examples=[580.00])

    created_at: datetime | None = Field(
        description="Created time", examples=[datetime.now(timezone.utc)]
    )

    created_by: str | None = Field(description="Created by User", examples=["System"])

    updated_at: datetime | None = Field(
        description="Updated time", examples=[datetime.now(timezone.utc)]
    )

    updated_by: str | None = Field(description="Updated by User", examples=["System"])

    model_config = {"from_attributes": True}


class OrderCreateDto(BaseModel):
    order_type_id: UUID | None = Field(
        description="order_type_id", examples=["EXasfew565d2"]
    )

    first_name_customer: str | None = Field(
        description="First Name", examples=["Phakkharaphong"]
    )

    last_name_customer: str | None = Field(
        description="Last Name", examples=["Charoenphon"]
    )

    phone: str | None = Field(description="phone", examples=["0943955615"])

    email: str | None = Field(description="email", examples=["example@gmail.com"])

    birth_date_customer_number: int = Field(
        description="Number for date", examples=[0]
    )

    birth_month_customer_number: int = Field(
        description="Number for month", examples=[0]
    )
    wallpaper_url: str = Field(
        description="wallpaper URL",
        examples=["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSD5EUXKEZYWRihvBte-enLd1V8C0OPK6lXKg&s"]
    )

    zodiac_customer_number: int = Field(
        description="Number for zodiac", examples=[0]
    )

    model_config = {"from_attributes": True}


class OrderUpdateDto(BaseModel):
    order_type_id: str | None = Field(
        description="order_type_id", examples=["EXasfew565d2"]
    )

    first_name_customer: str | None = Field(
        description="First Name", examples=["Phakkharaphong"]
    )

    last_name_customer: str | None = Field(
        description="Last Name", examples=["Charoenphon"]
    )

    phone: str | None = Field(description="phone", examples=["0943955615"])

    email: str | None = Field(description="email", examples=["example@gmail.com"])

    birth_date_customer_number: int | None = Field(
        description="Number for date", examples=[0]
    )

    birth_month_customer_number: int | None = Field(
        description="Number for month", examples=[0]
    )

    zodiac_customer_number: int | None = Field(
        description="Number for zodiac", examples=[0]
    )
    zodiac_customer: str | None = Field(
        description="Zodiac", 
        default="Rat"
    )

    payment_status: str | None = Field(
        description="payment_status", examples=["รอการชำระเงิน"]
    )

    wallpaper_url: str| None = Field(
        description="wallpaper URL",
        examples=["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSD5EUXKEZYWRihvBte-enLd1V8C0OPK6lXKg&s"]
    )
    model_config = {"from_attributes": True}


class OrderPromptPayQrDto(BaseModel):
    order_id: UUID = Field(description="Order id")
    amount: float = Field(description="Amount to pay")
    promptpay_id: str = Field(
        description="PromptPay recipient id (configured server-side)"
    )
    promptpay_payload: str = Field(
        description="EMV QR payload string (frontend can render QR from this)",
    )

class OrderPaymentGetDto(BaseModel):
    id: UUID | None = Field(description="order id", examples=["EXasfew565d2"])

    order_type_id: UUID | None = Field(
        description="order_type_id", examples=["EXasfew565d2"]
    )
    order_type: OrderTypeGetJoinDto | None = None

    first_name_customer: str | None = Field(
        description="First Name", examples=["Phakkharaphong"]
    )

    last_name_customer: str | None = Field(
        description="Last Name", examples=["Charoenphon"]
    )

    phone: str | None = Field(description="phone", examples=["0943955615"])

    email: str | None = Field(description="email", examples=["example@gmail.com"])

    payment_status: str | None = Field(
        description="payment_status", examples=["รอการชำระเงิน"]
    )

    birth_date_customer_number: int | None = Field(
        description="Number for date", examples=[0]
    )

    birth_month_customer_number: int | None = Field(
        description="Number for month", examples=[0]
    )

    zodiac_customer_number: int | None = Field(
        description="Number for zodiac", examples=[0]
    )

    total_price: float | None = Field(description="total_price", examples=[580.00])

    created_at: datetime | None = Field(
        description="Created time", examples=[datetime.now(timezone.utc)]
    )

    updated_at: datetime | None = Field(
        description="Updated time", examples=[datetime.now(timezone.utc)]
    )

    model_config = {"from_attributes": True}
