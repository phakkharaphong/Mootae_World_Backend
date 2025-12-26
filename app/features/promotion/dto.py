from datetime import datetime, date, timezone
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class PromotionGetDto(BaseModel):
    id: UUID | None = Field(
        description="order id", 
        default="EXasfew565d2"
    )
    
    promocode: str | None = Field(
        description="Promotion Code Format", 
        default="TE001"
    )
    
    promotion_title: str | None = Field(
        description="promotion title", 
        default="ส่วนลดตุรษจีน"
    )
    
    start_date: date | None = Field(
        description="Start Date", 
        default=date(2025, 8, 15)
    )
    
    end_date: date | None = Field(
        description="end Date", 
        default=date(2025, 8, 15)
    )
    
    discount: float | None = Field(
        description="discount", 
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

    model_config = {
        "from_attributes": True
    }


class PromotionGetOrderDto(BaseModel):
    
    promocode: str | None = Field(
        description="Promotion Code Format", 
        default="TE001"
    )
    
    promotion_title: str | None = Field(
        description="promotion title", 
        default="ส่วนลดตุรษจีน"
    )
    
    start_date: date | None = Field(
        description="Start Date", 
        default=date(2025, 8, 15)
    )
    
    end_date: date | None = Field(
        description="end Date", 
        default=date(2025, 8, 15)
    )
    
    discount: float | None = Field(
        description="discount", 
        default=580.00
    )
    
    

    model_config = {
        "from_attributes": True
    }


class PromotionCreateDto(BaseModel):
    promocode: str| None = Field(
        description="Promotion Code Format", 
        default="TE001"
    )
    
    promotion_title: str | None = Field(
        description="promotion title", 
        default="ส่วนลดตุรษจีน"
    )
    
    start_date: date | None = Field(
        description="Start Date", 
        default=date(2025, 8, 15)
    )
    
    end_date: date| None = Field(
        description="end Date", 
        default=date(2025, 8, 15)
    )
    
    discount: float | None = Field(
        description="discount", 
        default=580.00
    )
    
    is_active: bool | None = Field(
        description="Is Active", 
        default=True
    )
    # created_at: datetime | None = Field(
    #     description="Create at", 
    #     default_factory=datetime.now
    # )
    
    # created_by: str| None = Field(
    #     description="created by", 
    #     default="Admin"
    # )

    model_config = {
        "from_attributes": True
    }


class PromotionUpdateDto(BaseModel):
    promocode: str | None = Field(
        description="Promotion Code Format", 
        default="Tes51"
    )
    
    promotion_title: str | None = Field(
        description="promotion title", 
        default="ส่วนลดคนเก่ง"
    )
    
    start_date: date | None = Field(
        description="Start Date", 
        default=date(2025, 8, 15)
    )
    
    end_date: date | None = Field(
        description="end Date", 
        default=date(2025, 8, 15)
    )
    
    discount: float | None = Field(
        description="discount", 
        default=999.00
    )
    
    is_active: bool | None = Field(
        description="Is Active", 
        default=True
    )
    
    # updated_at: datetime | None = Field(
    #     description="Updated at", 
    #     default_factory=datetime.now
    # )
    
    # updated_by: str | None = Field(
    #     description="Updated by", 
    #     default="Admin"
    # )

    model_config = {
        "from_attributes": True
    }
