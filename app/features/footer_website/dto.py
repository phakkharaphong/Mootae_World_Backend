from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class FooterWebsiteGetDto(BaseModel):
    id: UUID | None = Field(
        description="Footer id", 
        default="EXasfew565d2"
    )
    
    title: str | None = Field(
        description="title icon", 
        default="วอลเปเปอร์เสริมดวง"
    )
    
    icon_img: Optional[str] | None = Field(
        description="icon img", 
        default="img/test.png"
    )
    
    link_ref: Optional[str] | None = Field(
        description="link ref", 
        default="www.example.com"
    )
    
    is_active: bool | None = Field(
        description="Is Active User", 
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


class FooterWebsiteCreateDto(BaseModel):
    title: str | None = Field(
        description="title icon",
        default="วอลเปเปอร์เสริมดวง"
    )
    
    icon_img: str | None = Field(
        description="icon img", 
        default="img/test.png"
    )
    
    link_ref: str | None = Field(
        description="link ref", 
        default="www.example.com"
    )
    
    is_active: bool | None = Field(
        description="Is Active User", 
        default=True
    )
    

    model_config = {
        "from_attributes": True
    }


class FooterWebsiteUpdateDto(BaseModel):
    title: str | None = Field(
        description="title icon",
        default="วอลเปเปอร์เสริมดวง"
    )
    icon_img: str | None = Field(
        description="icon img", 
        default="img/test.png"
    )
    
    link_ref: str | None = Field(
        description="link ref", 
        default="www.example.com"
    )
    
    is_active: bool | None = Field(
        description="Is Active User", 
        default=True
    )
    

    model_config = {
        "from_attributes": True
    }
