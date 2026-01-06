from uuid import UUID
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ContactUsGetDto(BaseModel):
    id: UUID | None = Field(
        description="Category id", 
        default="EXasfew565d2"
    )
    
    name: str | None = Field(
        description="Category Name", 
        default="สายมู"
    )

    email: str | None = Field(
        description="Email", 
        examples=["example@gmail.com"]
    )

    phone: str | None = Field(
        description="Phone", 
        examples=["0876119798"]
    )

    message: str | None = Field(
        description="message", 
        examples=["ทดสอบ"]
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


class ContactUsCreateDto(BaseModel):
    
    name: str | None = Field(
        description="Category Name", 
        default="สายมู"
    )

    email: str | None = Field(
        description="Email", 
        examples=["example@gmail.com"]
    )

    phone: str | None = Field(
        description="Phone", 
        examples=["0876119798"]
    )

    message: str | None = Field(
        description="message", 
        examples=["ทดสอบ"]
    )
    
    
    created_at: datetime | None = Field(
        description="Created time", 
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    created_by: str | None = Field(
        description="Created by User", 
        default="System"
    )


    model_config = {
        "from_attributes": True
    }
