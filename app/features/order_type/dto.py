from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field


class OrderTypeGetDto(BaseModel):
    id: UUID = Field(
        description="order_type id", 
        default="EXasfew565d2"
    )
    
    type_name: str | None = Field(
        description="type_name name", 
        default="Collection 1"
    )
    
    price: float | None = Field(
        description="price", 
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


class OrderTypeGetJoinDto(BaseModel):
    id: UUID = Field(
        description="order_type id", 
        default="EXasfew565d2"
    )
    
    type_name: str | None = Field(
        description="type_name name", 
        default="Collection 1"
    )
    
    price: float | None = Field(
        description="price", 
        default=580.00
    )

    model_config = {
        "from_attributes": True
    }


class OrderTypeCreateDto(BaseModel):
    type_name: str | None = Field(
        description="type_name name", 
        default="Collection 1"
    )
    
    price: float | None = Field(
        description="price", 
        default=580.00
    )
    
    is_active: bool | None = Field(
        description="Active status", 
        default=True
    )
    
    key: str = Field(
        description="key",
        examples=["love"]
    )

    model_config = {
        "from_attributes": True
    }


class OrderTypeUpdateDto(BaseModel):
    type_name: str | None = Field(
        description="type_name name", 
        default="Collection 1"
    )
    
    price: float | None = Field(
        description="price", 
        default=580.00
    )
    
    is_active: bool | None = Field(
        description="Active status", 
        default=True
    )
    

    model_config = {
        "from_attributes": True
    }
