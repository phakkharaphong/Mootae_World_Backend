from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field


class OrderPaymentGetDto(BaseModel):
    id: UUID | None = Field(
        description="order id", 
        examples=["EXasfew565d2"]
    )

    order_id: UUID | None = Field(
        description="order_id", 
        examples=["EXasfew565d2"]
    )
    
    amount: float | None = Field(
        description="amount", 
        examples=[580.00]
    )
    
    slip_url: str | None = Field(
        description="slip_url", 
        examples=["https://example.com/slip.jpg"]
    )
    
    payment_date: str | None = Field(
        description="payment_date", 
        examples=["2023-10-01T12:00:00Z"]
    )
    
    status: str | None = Field(
        description="status", 
        examples=["Pending"]
    )
    
    admin_note: str | None = Field(
        description="admin_note", 
        examples=["ตรวจสอบแล้ว"]
    )
    
    created_at: datetime | None = Field(
        description="Created time", 
        examples=[datetime.now(timezone.utc)]
    )

    model_config = {"from_attributes": True }


class OrderPaymentCreateDto(BaseModel):

    order_id: UUID = Field(
        description="order_type_id", 
        examples=["EXasfew565d2"]
    )
    
    amount: float = Field(
        description="amount", 
        examples=[580.00]
    )
    
    slip_url: str = Field(
        description="slip_url", 
        examples=["https://example.com/slip.jpg"]
    )
    
    model_config = {
        "from_attributes": True
    }