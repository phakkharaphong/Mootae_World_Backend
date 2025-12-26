from uuid import UUID
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class CategoryGetDto(BaseModel):
    id: UUID | None = Field(
        description="Category id", 
        default="EXasfew565d2"
    )
    
    name: str | None = Field(
        description="Category Name", 
        default="สายมู"
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


class CategoryCreateDto(BaseModel):
    name: str | None = Field(
        description="Category Name", 
        default="สายมู"
    )
    
    is_active: bool | None = Field(
        description="Is Active Category", 
        default=True
    )
    
    model_config = {
        "from_attributes": True
    }


class CategoryUpdateDto(BaseModel):
    name: str | None = Field(
        description="Category Name", 
        default="สายมู"
    )
    
    is_active: bool | None = Field(
        description="Is Active Category", 
        default=True
    )

    model_config = {
        "from_attributes": True
    }
