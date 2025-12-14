from datetime import datetime
from pydantic import BaseModel, Field


class OrderTypeGetDto(BaseModel):
    id: str = Field(
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
    
    is_active: bool | None = None
    
    created_at: datetime | None = Field(
        description="Created time", 
        default_factory=datetime.now
    )
    
    created_by: str | None = Field(
        description="created by", 
        default="Admin"
    )
    
    updated_at: datetime | None = None
    
    updated_by: str | None = None

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
    
    created_at: datetime = Field(
        description="Created time", 
        default_factory=datetime.now
    )
    
    created_by: str = Field(
        description="created by", 
        default="Admin"
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
    
    updated_at: datetime = Field(
        description="updated time", 
        default_factory=datetime.now
    )
    
    updated_by: str = Field(
        description="updated by", 
        default="Admin"
    )

    model_config = {
        "from_attributes": True
    }
