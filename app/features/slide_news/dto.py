from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SlideNewGetDto(BaseModel):
    id: str | None = Field(
        description="role id", 
        default="EXasfew565d2"
    )
    
    title: Optional[str] | None = Field(
        description="Title Slide New", 
        default="วอลเปเปอร์เสริมดวง"
    )
    
    link_ref: Optional[str] | None = Field(
        description="Link to page", 
        default="http:example.com"
    )
    
    img_path: Optional[str] | None = Field(
        description="Path Imge", 
        default="test/path/ssoKSm.png"
    )
    
    slide_number: Optional[int] | None = Field(
        description="slide number", 
        default=1
    )
    
    is_active: bool | None = None
    
    created_at: datetime | None = Field(
        description="Created time", 
        default_factory=datetime.now
    )
    
    created_by: Optional[str] | None = Field(
        description="created by", 
        default="Admin"
    )
    
    updated_at: datetime | None = None
    
    updated_by: Optional[str] | None = None

    model_config = {
        "from_attributes": True
    }


class SlideNewCreateDto(BaseModel):
    title: str | None = Field(
        description="Title Slide New", 
        default="วอลเปเปอร์เสริมดวง"
    )
    
    link_ref: str | None = Field(
        description="Link to page", 
        default="http:example.com"
    )
    
    img_path: str | None = Field(
        description="Path Imge", 
        default="test/path/ssoKSm.png"
    )
    
    slide_number: int | None = Field(
        description="slide number", 
        default=1
    )
    
    is_active: bool | None = None
    
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


class SlideNewUpdateDto(BaseModel):
    title: str | None = Field(
        description="Title Slide New", 
        default="วอลเปเปอร์เสริมดวง"
    )
    
    link_ref: str | None = Field(
        description="Link to page", 
        default="http:example.com"
    )
    
    img_path: str | None = Field(
        description="Path Imge", 
        default="test/path/ssoKSm.png"
    )
    
    slide_number: int | None = Field(
        description="slide number", 
        default=1
    )
    
    is_active: bool | None = None
    
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
