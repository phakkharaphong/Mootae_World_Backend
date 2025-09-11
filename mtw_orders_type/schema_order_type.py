from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class mtw_order_type(BaseModel):
    id: str = Field(
        description="order_type id",
        default="EXasfew565d2"
    )
    type_name: str |None = Field(
        description="type_name name",
        default="Collection 1"
    )
    is_active: bool | None = None
    created_at: datetime| None = Field(
        description="Created time",
        default_factory=datetime.now() 
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

class order_type_create(BaseModel):
    type_name: str | None = Field(
        description="type_name name",
        default="Collection 1"
    )
    is_active: bool | None = Field(
        description="Active status",
        default=True
    )
    created_at: datetime = Field(
        description="Created time",
        default_factory=datetime.now  # ✅ correct
    )
    created_by: str = Field(
        description="created by",
        default="Admin"
    )

    model_config = {
       "from_attributes": True
    }

class order_type_Response(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[mtw_order_type]