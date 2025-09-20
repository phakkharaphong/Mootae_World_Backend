from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class mtw_promotion(BaseModel):
    id: str| None = Field(
        description="order id",
        default="EXasfew565d2"
    )

    promocode: str |None = Field(
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
    discount: float |None = Field(
        description="discount",
        default=580.00
    )
    is_active: bool | None = None
    created_at: datetime| None = None
    created_by: str | None = Field(
        description="created by",
        default="Admin"   
    )
    updated_at: datetime | None = None
    updated_by: str | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class create_promotion(BaseModel):
    promocode: Optional[str] |None = Field(
        description="Promotion Code Format",
        default="TE001"
    )
    promotion_title: Optional[str] | None = Field(
        description="promotion title",
        default="ส่วนลดตุรษจีน"
    )
    start_date: Optional[date] | None = Field(
        description="Start Date",
        default=date(2025, 8, 15)
    )
    end_date: Optional[date] | None = Field(
        description="end Date",
        default=date(2025, 8, 15)
    )
    discount: Optional[float] |None = Field(
        description="discount",
        default=580.00
    )
    is_active: Optional[bool] | None = None
    created_at: Optional[datetime]| None = Field(
        description="Create at",
        default_factory=datetime.now
    )
    created_by: Optional[str] | None = Field(
        description="created by",
        default="Admin"   
    )
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class update_promotion(BaseModel):
    promocode: str |None = Field(
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
    discount: float |None = Field(
        description="discount",
        default = 999.00
    )
    is_active: bool | None = None
    updated_at: datetime| None = Field(
        description="Updated at",
        default_factory=datetime.now
    )
    updated_by: str | None = Field(
        description="Updated by",
        default="Admin"   
    )
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
